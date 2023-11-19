// Start with setting dates to pass into fetchEvents and for building the Calendar
var currentDate;
var nextDate;


//check for an existing date - we'll be setting a function to add/subtract a month based on listeners on the previous/next month button
if (!currentDate) {
  currentDate = new Date();
  nextDate = new Date();
}

// Get the first day of the current month so we can query the DB for events ranging within the month 2023-x-1 thru 2023-(x+1)-1
currentDate.setDate(1);
currentDate.setHours(0,0,0,0);
nextDate.setDate(1);
nextDate.setHours(0,0,0,0);

nextDate.setMonth(currentDate.getMonth() + 1);

// Because we aren't using timezone, we have to format the date
// Format the date as a string (e.g., "YYYY-MM-DD"):
let year = currentDate.getFullYear();
let month = String(currentDate.getMonth()+1).padStart(2, '0'); // Add 1 to the month because it's zero-based
let day = String(currentDate.getDate()).padStart(2, '0');
let formattedCurrentDate = `${year}-${month}-${day}`;

console.log(formattedCurrentDate);

// Format the date as a string (e.g., "YYYY-MM-DD"):
let yearNext = currentDate.getFullYear();
let monthNext = String(nextDate.getMonth() + 1).padStart(2, '0'); // Add 1 to the month because it's zero-based
let dayNext = String(nextDate.getDate()).padStart(2, '0');
let formattedNextDate = `${yearNext}-${monthNext}-${dayNext}`;
console.log(formattedNextDate);

fetch(`/fetchEvents?currentDate=${formattedCurrentDate}&nextDate=${formattedNextDate}`,{
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
         },
         body: JSON.stringify({}),
     })
      .then(response => response.json())
      .then(data => {
          // Display the API response
          //responseDiv.innerHTML = JSON.stringify(data, null, 2);
          console.log(data);
      })
      .catch(error => {
          console.error(error);
      });

// Calendar Creation

async function createCalendar() {
// Get references to DOM elements
const monthYearElement = document.getElementById("monthYear");
const daysTable = document.getElementById("days");
const datesTable = document.getElementById("dates");
const prevMonthButton = document.getElementById("prevMonth");
const nextMonthButton = document.getElementById("nextMonth");

// Initialize the calendar with the current month - BL - moved to top
// var currentDate = new Date();

// Function to generate the calendar for a given month
function generateCalendar(year, month) {
  // Clear existing calendar content
  daysTable.innerHTML = "";
  datesTable.innerHTML = "";

  // Set the current date to the first day of the month
  const firstDay = new Date(year, month, 1);

  // Set the header to display the current month and year
  monthYearElement.textContent = `${firstDay.toLocaleString('default', { month: 'long' })} ${year}`;

  // Create the day headers (Sun, Mon, Tue, etc.)
  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const daysRow = daysTable.insertRow();
  daysOfWeek.forEach(day => {
    const cell = daysRow.insertCell();
    cell.textContent = day;
  });

  // Get the number of days in the current month
  const lastDay = new Date(year, month + 1, 0).getDate();

  // Calculate the day of the week on which the first day falls
  const startDay = firstDay.getDay();
  
  // Create the Events
  var events = jsonData.data;
  
  // Create the calendar dates
  let date = 1;
  for (let i = 0; i < 6; i++) { // 6 rows for maximum
    const row = datesTable.insertRow();
    for (let j = 0; j < 7; j++) {
      if (i === 0 && j < startDay) {
        const cell = row.insertCell();
        cell.textContent = "";
      } else if (date <= lastDay) {
        const cell = row.insertCell();
        cell.textContent = date;
        for (let k = 0; k < events.length; k++) {
          var eventDate = new Date(events[k].startTime);
          if (eventDate.getDate() == date && eventDate.getMonth() == month && eventDate.getYear() == year) {
            cell.textContent = events[k].fName;
            cell.style.backgroundColor = "blue";
          }
        }
        date++;
      }
    }
  }
}

 // Insert the data into the calendar dates
 // date = the date, and insert using the above for loop
 // need to get the format of the json. Run another for loop thru the events. If date matches, then insert in line 102 with the cell content.
  
  
// Function to go to the previous month
function previousMonth() {
  currentDate.setMonth(currentDate.getMonth() - 1);
  generateCalendar(currentDate.getFullYear(), currentDate.getMonth());

}

// Function to go to the next month
function nextMonth() {
  currentDate.setMonth(currentDate.getMonth() + 1);
  generateCalendar(currentDate.getFullYear(), currentDate.getMonth());

}

// Attach click event handlers to the navigation buttons
prevMonthButton.addEventListener("click", previousMonth);
nextMonthButton.addEventListener("click", nextMonth);

// Initialize the calendar
document.addEventListener("DOMContentLoaded", function(event) { 
  generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
});
}

//Added 11/17/23 console log from API pulled from Python
console.log('from calendar.js');
console.log(jsonData);
createCalendar();

/* For fetching events using javascript
// Pull the data for the calendar events for the month/year
async function fetchEvents() {

  //set up the dates
  var currentDate;
  var nextDate;

  //check for an existing date - we'll be setting a function to add/subtract a month based on listeners on the previous/next month button
  if (!currentDate) {
    currentDate = new Date();
  }
  console.log(currentDate);

  nextDate = currentDate;
  nextDate.setMonth(currentDate.getMonth() + 1);

  // Get the first day of the current month
  currentDate.setDate(1);
  currentDate.setHours(0,0,0,0);
  console.log('currentDate is '+currentDate);
  console.log('nextDate is '+nextDate);

  // Format the date as a string (e.g., "YYYY-MM-DD"):
  let year = currentDate.getFullYear();
  let month = String(currentDate.getMonth()).padStart(2, '0'); // Add 1 to the month because it's zero-based
  let day = String(currentDate.getDate()).padStart(2, '0');
  let formattedCurrentDate = `${year}-${month}-${day}`;

  console.log(formattedCurrentDate);

  // Format the date as a string (e.g., "YYYY-MM-DD"):
  let yearNext = currentDate.getFullYear();
  let monthNext = String(currentDate.getMonth() + 1).padStart(2, '0'); // Add 1 to the month because it's zero-based
  let dayNext = String(currentDate.getDate()).padStart(2, '0');
  let formattedNextDate = `${yearNext}-${monthNext}-${dayNext}`;
  console.log(formattedNextDate);

  console.log('fetchEvents for Calendar script')
      var { data, error } = await supabase
        .from('reservations')
        .select()
        .gte('startTime', formattedCurrentDate)
        .lt('startTime', formattedNextDate)



    if (error) {
        console.error('Error fetching data:', error);
    } else {
        console.log('Fetched data:', data);
    }

}

fetchEvents();
*/