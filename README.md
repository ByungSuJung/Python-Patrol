# Python-Patrol
This is a class project that our team (Python Patrol) has created at University of Washington Bothell, the specific coure this is for is fundamentals of computer simulation theory and application.

Project description:
	This project simulates traffic in any location on earth. Cars are set to have random starting points and destinations. The goal of this project is to study the effect on traffic by calculating weight on edges using different capacity/time step ratio. The program also provide visualization option (may be laggy).


Pre-Request:
1.	Install osmnx package
	‘conda install -c conda-forge osmnx’
	OR ‘pip install osmnx’
2.	Git clone https://github.com/T-Wick/Python-Patrol
3. 	(Parallel branch only) pip install joblib

Running the project:
	‘python driver.py’

User-adjustable variables:
	User adjustable variables are located in driver.py
	Size - list of car numbers desired to simulate. It can hold a list with single value if single car size size simulation is desired. The program will iterate through size and run simulations.
	Weights_ratio - list of ratio desired to simulate. The number should be in [0.0:1.0]. Any number outside of the range is not promised to run properly.
	Place_coord - the longitude and altitude of the map center. Default is Seattle Downtown.
	Map_size - the radius of the map, default is 15000
	Visual - if visual is true, the program will use the first number in size and weights_ratio and provide animation. (only one simulation runs if visual is true). Suggest turning visual off if doing analysis only
	CORES - number of CPU CORE desired to compute. -1 represents all cores, -2 represents all cores except the first one. A number > actual core number will result in running on single core.
	Console_output - if true, the program will print information on the terminal.
	FILE_OUTPUT_NAME - str, path to log file. Log file will record information during the simulation.
