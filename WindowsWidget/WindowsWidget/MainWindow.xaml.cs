using System;
using System.ComponentModel;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Threading;
using OpenHardwareMonitor.Hardware;
using System.Runtime.CompilerServices;
using CoreAudio;

namespace WindowsWidget
{
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        private readonly DispatcherTimer _timer;

        // Current time
        private string _currentTime = DateTime.Now.ToString("hh:mm:ss tt");

        // For switching between devices
        private int audio = 0;

        // GPU temperature
        private double _gpuTemperature;
        public double GPUTemperature
        {
            get { return _gpuTemperature; }
            set { _gpuTemperature = value; OnPropertyChanged(); }
        }

        private readonly Computer _computer = new Computer();

        public static class AudioSwitch
        {
            // Set audio device
            public static void SetDefaultDevice(string id)
            {
                MMDeviceEnumerator deviceEnum = new MMDeviceEnumerator(Guid.NewGuid());
                MMDevice device = deviceEnum.GetDevice(id);
                deviceEnum.SetDefaultAudioEndpoint(device);
            }

            // Get audio devices
            public static MMDeviceCollection GetAudioDevices()
            {
                MMDeviceEnumerator deviceEnum = new MMDeviceEnumerator(Guid.NewGuid());
                return deviceEnum.EnumerateAudioEndPoints(DataFlow.Render, DeviceState.Active);
            }
        }


        public MainWindow()
        {
            InitializeComponent();

            // Program always on display
            this.Topmost = true;

            // Set initial window position
            // Change left value to 1420 if for single window
            Left = 3340;
            Top = 850;

            DataContext = this;

            // Initialize OpenHardwareMonitor and GPU monitoring
            _computer.Open();
            _computer.GPUEnabled = true;

            // Calls UpdateGPUTemperature 
            UpdateGPUTemperature();

            // Initialize and start the timer for periodic updates
            _timer = new DispatcherTimer();
            _timer.Interval = TimeSpan.FromSeconds(30); // Update every 30 seconds
            _timer.Tick += OnTimerTick;
            _timer.Start();

            // Start a background task to continuously update the time
            Task.Run(() =>
            {
                while (true)
                {
                    CurrentTime = DateTime.Now.ToString("hh:mm:ss tt");
                    Thread.Sleep(50);
                }
            });
        }

        // Update GPU Temperature
        private void UpdateGPUTemperature()
        {
            // Enable GPU monitoring
            _computer.GPUEnabled = true;

            // Update hardware sensor data
            _computer.Hardware[0].Update();

            // Find and update GPU temperature sensor
            var gpuTempSensor = _computer.Hardware.FirstOrDefault(h => h.HardwareType == HardwareType.GpuNvidia)?.Sensors.FirstOrDefault(s => s.SensorType == SensorType.Temperature);

            // Get GPU temperature
            if (gpuTempSensor != null)
            {
                var gpuTempValue = gpuTempSensor.Value ?? 0;
                GPUTemperature = gpuTempValue;
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        // Current time
        public string CurrentTime
        {
            get { return _currentTime; }
            set
            {
                _currentTime = value;
                OnPropertyChanged(nameof(CurrentTime));
            }
        }

        // Updates time and GPU temperature
        private void OnTimerTick(object? sender, EventArgs e)
        {
            // Update GPU temperature and current time
            UpdateGPUTemperature();
            CurrentTime = DateTime.Now.ToString("hh:mm:ss tt");
        }

        // Change audio output
        private void AudioOutputButton_Click(object sender, RoutedEventArgs e)
        {
            MMDeviceCollection devices = AudioSwitch.GetAudioDevices();

            if (audio == devices.Count() + 1)
            {
                audio = 0;
            }

            MMDevice defaultDevice = devices[audio];

            Console.WriteLine("Setting default audio device...");
            AudioSwitch.SetDefaultDevice(defaultDevice.ID);

            audio++;
        }
    }
}
