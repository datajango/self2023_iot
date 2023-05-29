import wx
import logging
from mqtt_monitor.config_manager import ConfigurationManager
from main_window import MainWindow
from logger import setup_logger

def main():
    logger = setup_logger("log", "logfile.log")    
    config_manager = ConfigurationManager("settings.json")

    app = wx.App(False)    
    frame = MainWindow(None, 'MQTT Monitor', config_manager, logger)
    frame.Show(True)

    logger.info("mqtt_monitor created by Anthony Leotta")
    app.MainLoop()

if __name__ == '__main__':
    main()