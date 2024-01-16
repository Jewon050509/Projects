# For todolist
```bash
pip install -r requirements.txt
```
And run
```bash
python main.py
```
The program should be on http://127.0.0.1:5000



# For WindowsWidget
On NuGet Package Manager, install:
* CoreAudio
* OpenHardwareMonitor.Core
* System.Management

Unless you have two monitors, you may want to change
```bash
this.Topmost = true;
```
To false:
```bash
this.Topmost = true;
```

You may need to change Left value on MainWindow.xaml.cs (Line 62) for different monitor setup. Use 1420 for single monitor.
