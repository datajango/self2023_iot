import wx
from wx_mqtt_control.mqtt_broker_manager import BrokerManager
from wx_mqtt_monitor.config_manager import ConfigurationManager
from main_window import MainWindow
from logger import setup_logger
from wx_mqtt_control.__version__ import __version__

def main():
    logger = setup_logger("log", "logfile.log")    
    config_manager = ConfigurationManager("settings.json")
    broker_manager = BrokerManager(config_manager)
    
    app = wx.App(False)    
    frame = MainWindow(None, 
                       f'MQTT Control {__version__}', 
                       config_manager, 
                       broker_manager,
                       logger)
    frame.Show(True)

    logger.info(f"MQTT Control {__version__} created by Anthony Leotta")
    logger.info(f"Copyright (C) 2023 Anthony Leotta")
    app.MainLoop()

if __name__ == '__main__':
    main()