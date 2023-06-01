import os
import json
import logging
import getpass
import wx

from wx_mqtt_monitor.forms.error_indicator import ErrorIndicator

class DebugGridBagSizer(wx.GridBagSizer):
    def Draw(self, dc):
        for row in range(self.GetRows()):
            for col in range(self.GetCols()):
                pos = self.GetPositionOfCell(row, col)
                size = self.GetCellSize(row, col)
                dc.SetPen(wx.Pen('red', 1, wx.PENSTYLE_SOLID))
                dc.DrawRectangle(pos, size)

        super().Draw(dc)
        
def create_red_dot(size=10):
    # Create an empty image
    image = wx.Image(size, size)

    # Set all pixels to red
    for x in range(size):
        for y in range(size):
            image.SetRGB(x, y, 255, 0, 0)

    # Convert the image to a bitmap
    bitmap = wx.Bitmap(image)

    return bitmap

def create_red_dot_v2(size=10):
    # Create an empty image
    image = wx.Image(size, size)

    # Create transparency mask (all pixels are transparent by default)
    mask = wx.AlphaChannel(image)
    mask.Clear(0)  # Clear all alpha to make it fully transparent
    
    # Set all pixels in a circle to red
    radius = size / 2
    for x in range(size):
        for y in range(size):
            dx = x - radius
            dy = y - radius
            if dx*dx + dy*dy <= radius*radius:  # Pixel is inside circle
                image.SetRGB(x, y, 255, 0, 0)  # Set pixel to red
                mask.SetValue(x, y, 255)  # Make pixel opaque

    # Apply the alpha mask to the image
    image.SetAlpha(mask)

    # Convert the image to a bitmap
    bitmap = wx.Bitmap(image)

    return bitmap

def create_red_dot_v3(size=10):
    # Create a new empty bitmap of the required size
    bitmap = wx.Bitmap(size, size)

    # Create a "MemoryDC" to draw on the bitmap
    dc = wx.MemoryDC(bitmap)

    # Make the DC's background transparent
    dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, alpha=wx.ALPHA_TRANSPARENT)))
    dc.Clear()

    # Create a GraphicsContext from the DC
    gc = wx.GraphicsContext.Create(dc)

    # Set the brush for filling the circle to red
    brush = gc.CreateBrush(wx.Brush("RED"))
    gc.SetBrush(brush)

    # Draw a circle at the center of the bitmap
    gc.DrawEllipse(0, 0, size, size)

    # Delete the DC to finish drawing on the bitmap
    del dc

    return bitmap

def get_form_definition_paths(file_name, additional_paths=None):
    form_definition_paths = []

    if additional_paths is not None:
        for path in additional_paths:
            if not os.path.exists(path):
                raise ValueError(f"Path {path} does not exist")                                
            form_definition_paths.append(os.path.join(path, file_name))
        
    # Get username and home path
    username = getpass.getuser()
    home_path = os.path.expanduser("~")

    # Check environment variable
    env_path = os.getenv('FORM_PATH')
    if env_path:
        form_definition_paths.append(os.path.abspath(env_path))

    # Check current working directory
    form_definition_paths.append(os.path.join(os.getcwd(), file_name))

    # Check user's home directory
    form_definition_paths.append(os.path.join(home_path, file_name))

    # Add further custom locations as per requirements here.

    return form_definition_paths


def load_json_file(file_name, additional_paths=None):
    """Load the form definition from the default location"""
    paths = get_form_definition_paths(file_name, additional_paths)
    
    for path in paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    form_definition = json.load(f)
                    logging.info(f"Form definition loaded successfully from {path}")
                    return form_definition
        except IOError as e:
            logging.error(f"IOError while loading form definition: {str(e)}")
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in form definition file: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error while loading form definition: {str(e)}")

    logging.warning(f"Form definition file not found in locations: {paths}, using default form definition.")
    return {}  # Return an empty dictionary as the default form definition, adjust as needed


class TextField:
    def __init__(self, 
                 parent, 
                 label_text, 
                 input_length,
                 validation_rules, 
                 entry_args=None, 
                 entry_kwargs=None):
        self.parent = parent
        self.label_text = label_text
        self.input_length = input_length
        self.validation_rules = validation_rules
        self.entry_args = entry_args
        self.entry_kwargs = entry_kwargs
        self.error_indicator = None

    def validate(self):
        value = self.input.GetValue()
        valid = True
        if self.validation_rules.get('type') == 'length':
            min_length = self.validation_rules.get('min', 0)
            max_length = self.validation_rules.get('max', float('inf'))
            if not (min_length <= len(value) <= max_length):
                valid = False

        self.set_error(not valid)

        return valid

    def renderField(self):

        self.label = wx.StaticText(self.parent, -1, self.label_text)
        
        self.input = wx.TextCtrl(self.parent, -1, "")
        self.input.Bind(wx.EVT_TEXT, self.on_text_changed)
        self.input.Bind(wx.EVT_KILL_FOCUS, self.on_text_changed)

        self.error_indicator= ErrorIndicator(self.parent)

        self.validate()  # Validate the field initially to set the error indicator

        return self.label, self.input, self.error_indicator

    def set_error(self, has_error):
        if has_error:
            self.error_indicator.set_error_state(True)
        else:
            self.error_indicator.set_error_state(False)

    def on_text_changed(self, event):
        text = event.GetEventObject().GetValue()
        if not self.validate():
            self.error_indicator.set_error_state(True)
        else:
            self.error_indicator.set_error_state(False)
        event.Skip()  # important to ensure correct event propagation

class FormManager():
    def __init__(self) -> None:
        self.form_sizer = None
        self.form_fields = None
        self.form_data = None

    def load_form_definition(self, filename, additional_paths=None):
        self.form_data = load_json_file(filename, additional_paths)

    def calc_width(self, input_length, input):
            """  Calculate the minimum width of the input field based on the font size """
            font = input.GetFont()
            font_size = font.GetPointSize()
            char_width = font_size * 0.6  # Adjust the multiplier based on font and preferences
            width = int(input_length * char_width)
            return width
            
    def create_form(self, parent):
        """Create form fields from form_definition and return a wx.Sizer with the complete form layout."""

        if self.form_data is None:
            raise ValueError("Form definition not loaded. Call load_form_definition() first.")
        
        fields = []

        # Extract the form_fields from form_definition
        form_fields = self.form_data.get("form_fields", [])
        num_rows = len(form_fields)
        self.form_sizer = wx.FlexGridSizer(num_rows, 3, 15, 20) 

        for i, field_definition in enumerate(form_fields):
            if field_definition["type"] == "TextField":
                label_text =  field_definition.get("label", f"Text Input {i+1}:")
                validation_rules = field_definition.get("validation_rules", {})
                input_length = field_definition.get("input_length", 10)

                field = TextField(parent, 
                                  label_text,
                                  input_length,
                                  validation_rules)                            
            else:
                raise ValueError(f"Unsupported field type: {field_definition['type']}")
    
            fields.append(field)
            
            label, input, error_indicator = field.renderField()  
            
            width = self.calc_width(input_length, input)
            input.SetMinSize((width, -1))  # Set the desired minimum width
            
            self.form_sizer.Add(label)
            #self.form_sizer.Add(input, flag=wx.EXPAND)
            self.form_sizer.Add(input)
            self.form_sizer.Add(error_indicator)

        

        # Make sure the sizer recalculates its layout now that we've added all the controls
        self.form_sizer.Layout()