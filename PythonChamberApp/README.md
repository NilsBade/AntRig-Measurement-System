![AntRig Logo](/figures/logos/AntRig_Logo_Large.svg)
# PythonChamberApp - GUI Walk-through
## 1. Config Tab
![Config_Tab](/PythonChamberApp/figures/Readme/AntRig_ConfigTab_annotated.svg)

1. Input IP-adress associated with the AntRig chamber in your network.
2. Input API-key (provided/created in octoprint) that enables access to chamber (printer) controls.
When pressing the 'Connect' button below, a request is sent to the chamber and the printer hardware is set active.
For the procedure IP and API-key must be valid. Details are written to the terminal (7) on the right.
3. Application searches for available VISA devices connected to the host computer. The information is written to the terminal (7) on the right and the dropdown (4) is updated with the selectable devices.
4. Dropdown menu to select one of the detected VISA interfaces/adresses.
5. When 'Connect ? IDN' is pressed, an IDN request is sent to the VISA equipment selected in the dropdown (4) above. 
The device's answer is written to the terminal (7) on the right.
6. If the checkbox is selected, the pyVISA instance is started with explicit 'ktvisa32' configuration. This _should_ result in the keysight backend being used. However, this option seems to misbehave/have no impact on the execution (tested with pyvisa package version 1.15.0). Therefore, this option can be ignored at the moment...
7. Terminal, that collects information about every communication with external devices. It updates when functionality within the config-tab is used, and logs all updates sent during/by Auto Measurement processes.
8. Clears the terminal (7) above.

## 2. Chamber Control Tab
![Chamber_Tab](/PythonChamberApp/figures/Readme/AntRig_ChamberControlTab_annotated.svg)

1. When 'Home all axis' is pressed, firstly the user is asked whether the z-limit switch is mounted to the chamber. If confirmed, the AntRig chamber is requested to home all axis. Thereby, the probe head first runs into the x-limit switch, then the y-limit switch als lastly the base plate is moved up until the z-limit switch ([BL-Touch sensor](/docs/BOM/BLTouch-Datasheet.pdf)) is triggered. __This home-procedure must be done every time the AntRig System (Chamber!) is turned on!__ Afterwards the PythonChamberApp and the Printer-system (= Klipper = Chamber) initialize their position and the mechanical system can be controlled and used.
_(Only exception explained in (9), 'Restore App's Position from Log')_

> [!CAUTION]
> The printer hardware does not differentiate between a not-wired and a not-triggered BL-Touch sensor! Thus the base plate will collide with its upper bearings in case the setup lacks the z-limit switch and homing is issued!

2. The 'Z-Tilt-Adjustment' is an automatic leveling-procedure provided by Klipper for Core-XY configurations. This process aligns the base plate horizontally by probing the base plate close the three lead-screws. Differences are measured by the z-limit switch and all three bearing points are aligned to the same height one by one. __Before issuing the alignment, make sure the base plate is roughly horizontal, to avoid the base plate bearings collide with the upper lead-screw constraints and the probe head/BL-Touch sensor collide with the base plate when hovering 1cm above it.__  When this button is pressed, the user is asked to confirm that the BL-Touch sensor is mounted, before the procedure is started.
3. Here a custom home-position in [X,Y,Z] can be saved in the textfields. One can move back to this position automatically by pressing the "home-buttons" below - seperated in regards to z-direction (base plate only) or xy-plane (probe head only).
4. The arrow buttons allow to issue relative movement of the probe head/chamber. Thereby the stepsize can be configured manually (5) and the movement speed (6) as well.
5. Input of stepsize for relative movement (4) in [mm].
6. Input of movement speed for relative movement and movements issued via 'GoTo' (7) in [mm/s].
7. Inputs to move to absolute chamber-coordinates instead of relative movement. When 'Go' is pressed, the probe head moves to the input [X,Y,Z] coordinates.
8. Log terminal that collects all movement commands sent to the AntRig Chamber. This holds for funcionality within this tab and all commands sent during an Auto Measurement process.
9. 'Restore App's Position from Log' allows to override the current PythonChamberApp-position with the [X,Y,Z] coordinates defined in the _'cur_position_log.json'_ file, located in the upper _PythonChamberApp_ directory (same directory as this Readme-file).

> [!NOTE] 
> 'Restore App's Position from Log' helps, in case the chamber setup stays in operation while the PythonChamberApp is restarted (for some reason). In that case, the app forgets the current probe head position and forces the user to home all axes before any other chamber operation is enabled. However, Klipper, executed on the chamber hardware, still knows the current position, and normal operation would be possible without homing the setup. Therefore, the PythonChamberApp stores its current position by overriding the _'cur_position_log.json'_ file after every movement request that is sent to the chamber. This option might be helpful in cases where a complex setup is mounted to the base plate and homing the entire setup is not feasible or undesired, while some modification of the app is required; thus, restarting the app is inevitable.

10. Live position view that shows the current position of the setup at all time. The blue plane represents the base plate and the light-blue frame represents the probe. The axes show the chamber-COS-directions: X - red, Y - green, Z - blue.
11. 3D visualization of the chamber setup. The origin is marked by the three colored axes. The red frame shows the borders of the working volume of the chamber. The blue plane represents the position of the base plate and the white dots show the position of the probe head in the XY plane. The slim volume/section at the top of the red-lined-frame corresponds to the minimal distance between the base plate surface at hightes position and the down-facing mounting-plane of the probe head. The references are visualized in the picture below.
![WorkingVolume_visualization](/PythonChamberApp/figures/Readme/AntRigChamber_WorkingVolumeVisualization.svg)

## 3. VNA Control Tab (Measurement Equipment)
![VNA_Tab](/PythonChamberApp/figures/Readme/AntRig_VNAControlTab_annotated.svg)

1. Textfield to input custom VISA commands.
2. Sends the input command (1) as read-request to the VNA device.
3. Sends the input command (1) as write-request to the VNA device.
4. Sends the input command (1) as query-request to the VNA device.
5. Terminal that logs the sent VISA commands and the received answers from the VNA.
6. Clears the terminal (5) above.

## 4. Auto Measurement Tab
![AutoMeas_Tab](/PythonChamberApp/figures/Readme/AntRig_AutoMeasurementTab_annotated.svg)

1. Input for the length of the probe antenna, measured from the mounting-surface of the probe head (= bottom side) to the tip of the probe. This parameter is used to update the length of the upper, light-blue box in the 3D visualization (22) that represents the probe.
2. Input for the length/height of the Antenna under test (AUT). Height is measured from base plate surface to tip of the AUT aperture. This parameter is used to update the height of the lower, light-blue box in the 3D visualization (22) that represents the AUT.
3. Pressing this button, the standard XY center coordinate (_hardcoded in [process controller object](/PythonChamberApp/PythonChamberApp/process_controller/process_controller.py)) is set for [X,Y] of the zero-position. The Z coordinate is calculated from "$ProbeLength + AUTHeight - MinProbeHeadToBasePlateDistance$", which corresponds to the ideal position in which the antenna tips should touch each other.

> [!Note] 
> The 'zero-position' is the coordinate, in which the AUT and the probe are aligned with their XY centers and their tips touch each other (~ z-coordinate). In reference to this position, the measurement volume is defined and all coordinates for the Auto Measurement process are calculated. Moreover, all plots (22), (23) and (24) only update once a zero-position is defined.

4. Movement speed in [mm/s] which is used during the Auto Measurement process.
5. Moves the probe __1cm above__ the currently set zero-position.
6. Overrides the zero-position with the current probe position/coordinates.
7. Live display of the current probe position and the currently set zero-position.
8. Dropdown menu for selecting a measurement mesh configuration scheme. In the PythonChamberApp V1 only a cubic mesh is available.
9. Dropdown menu for selecting the order in which the X,Y and Z axes are to be traversed during the Auto Measurement.
10. Dropdown  menu for selecting the movement pattern. 'line-by-line' transverses the axes, always starting at the minimum coordinate and moving to the maximum. In contrast, 'snake' always moves to the next closest point. Thus for example going '_x_min > x_max > [y++] > x_max > x_min > ..._'. Thereby, the plane in which the snake pattern is realised is span by the first two axes, selected in the axes order (9).

> [!Note]
> The movement pattern influences the movement/position of all signal-paths as well. When working with the different movement pattern, systematic errors in phase and amplitude were experienced that align with the changing movement directions and consequently changing HF-cable positions. This error is highly dependent on the exact positioning/routing of the cables and the selected hardware. Thus the significance of this error must be evaluated individually. However, due to the shorter travel distances of the probe, the snake-pattern reduces the overall measurement time which scales with the number of measurement points.

11. Input fields to configure the measurement volume and mesh. After every modification, the displays in (22), (23), (24) are updated.
12. These limit values update every time the zero-position is (re-)set. The maximum possible measurement volume dimensions are calculated based on the available working volume and the current zero-position in chamber coordinates.
13. Dropdown menu for selecting whether the VNA (_= measurement equipment_) is configured via a config file, saved locally on the VNA (Input field (15)), or by manual, custom inputs (16). Dependent on the selection, inputs in (15) or (16) are disabled/enabled.
14. Timeout value in [ms] for the VISA communication _Measurement Equipment <> PythonChamberApp_. After this timeout, the communication times out on PythonChamberApp-side and an error is thrown. This timeout must be adapted to account for the required measurement-duration of the VNA (_= measurement equipment_). If this paramete is set too low, the app times out while the VNA still measures, resends its commands and all data is repetitivly lost. In that case the measurement must be stopped by the user via the 'Stop Measurement' button (21).
15. Inputs to set the path to the config file stored locally on the VNA. The check button sends the config-request to the VNA and the user can check whether all parameters are set correctly and the VNA is operational. The set parameters are shown in (16), updated according to the restored VNA-configuration.
16. Custom input fields to configure the VNA measurement with typical parameters. Units are listed in the corresponding lines.
17. Input field for the name of the measurement file that will be saved. The '.json' ending will be added automatically. In case a file already exist with the given file name in the _results_ directory, an error is asserted and the file name must me modified. It is not possible to override any result file through the app.
18. Checkbox to select whether a 4-whitespace indent should be used in the file (improves direct readability) or not.
19. Start Button for the Auto Measurement process. This button is enabled once the zero position is defined. When clicked, the validity of the measurement mesh, (partly) the VNA configuration and the file name is checked. In case of errors occur, they will be shown in a pop-up window.
20. The _Auto Measurement Progress_ display shows the live progress of running Auto Measurements. Based on the average time taken per measurement point, the 'Time to go' is re-estamiated after each taken measurement. Consequently, the prediction becomes more accurate with every point measured and is valid once a repeating mesh sequence is completed.
21. The 'Stop Measurement' button allows for interruption of the currently running measurement without loss of acquired data. When pressed, the user is firstly asked to confirm the decision. If confirmed, the (so far) acquired data is saved to the desired json file, a pop-up window shows the exact file location and the taken measurement time and afterwards all app functionalities are re-enabled.
22. 3D visualization of the configured measurement mesh in reference to the available chamber working volume.
23. XY top view on the configured measurement mesh in reference to the available chamber working volume. The axes show absolute chamber coordinates and the thick, blue dot shows the location of the current zero-position in reference to the working volume.
24. XZ front view on the configured measurement mesh in reference to the available chamber working volume. The axes show absolute chamber coordinates and the thick, blue dot shows the location of the current zero-position in reference to the working volume.

> [!Note]
> The dots in all plots (22), (23), (24) mark the combination of "xy = position of probe in plane, z = top end of AUT". T

## 5. Display Measurements Tab
![DispMeas_Tab](/PythonChamberApp/figures/Readme/AntRig_DisplayMeasurementsTab_annotated.svg)

1. Dropdown menu for selection of the available result measurement files in the _results_ directory. This menu must be updated via the Refresh button (2) first.
2. Updates the file-selection dropdown menu on the left (1) according to the files located in the _results_ directory.
3. Reads the file selected in the dropdown menu (1) to the app's data buffer, updates the info terminal (4), enables all user interactions (5),(6),(7),(8),(9) and updates the plots (10).
4. Terminal shows the information given in the 'measurement config' field of the read measurement file. For example set zero-position (in chamber coordinates), measurement duration, configured mesh, etc.
5. Dropdown menu for selection of the S-parameter that is supposed to be displayed in the plots (10). The dropdown menu options update according to the available data in the read mesurement file.
6. Slider and textfield to select the frequency that is supposed to be displayed in the plots (10).
7. Dropdown mennu to select whether linear or db scale should be displayed in the amplitude plots below (10).
8. Checkbox to select whether absolute chamber coordinates or relative AUT-coordinates (= ref _zero-position_) should be displayed on the plots' axes (10).
9. Slider to select the x,y,z coordinate of each cut-view in the plots below (10). Every slider affects the two plots (amplitude and phase) below itself.
10. Cut-view plots of measured amplitude and phase data. The toolbars at the bottom allow for manual modification of the displayed data like rescaling the heatmaps or zooming into a section of interest. The axes/view of the amplitude and phase plots that belong to the same cut-view (XZ or YZ or XY) are linked. Thus, the cut-views always show amplitude and phase values that correspond to the same spatial section from the data-space. 