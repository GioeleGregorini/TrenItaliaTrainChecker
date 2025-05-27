# Real-Time Train Monitoring

This Python project allows you to monitor the real-time status of a train using data from the ViaggiaTreno website by Trenitalia. The application fetches information about a specific train, such as delays, scheduled and actual departure times, the last tracking information, and the latest exit time from the station based on delays.

## Key Features:
- **Real-Time Monitoring:** Track delays, scheduled and actual departure times of a train.
- **Tkinter GUI:** The app has a simple graphical interface displaying data clearly and intuitively.
- **Automatic Updates:** The page updates automatically to reflect the most recent data available on Trenitalia’s website.
- **Latest Exit Time Calculation:** It calculates the latest time you can leave the station based on the train’s delay, so you don’t miss the train.
- **Visual Feedback:** A status label indicates when data is being retrieved, and when updates are successfully completed or if an error occurs.

## How it works:
1. **Enter the train number:** Input the train number you want to monitor into the graphical interface’s input box.
2. **Data retrieval:** The app sends a request to the ViaggiaTreno website to fetch the train details.
3. **Display Data:** It shows information like the scheduled departure, actual departure, delay, and last tracking info.
4. **Automatic Updates:** If the train status changes, the interface updates automatically.

## Technologies Used:
- **Python 3** with the following libraries:
  - `Tkinter`: for the graphical interface.
  - `requests`: for making HTTP requests to the ViaggiaTreno website.
  - `BeautifulSoup`: for parsing the HTML content of the webpage.
  - `re`: for extracting data using regular expressions.
  - `datetime`: for calculating the latest exit time from the station.

## How to Run the Project:
1. Clone the repository:
   ```bash
   git clone https://github.com/GioeleGregorini/TrenItaliaTrainChecker.git
