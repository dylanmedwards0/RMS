import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

//const supabase = createClient('{{ url }}', '{{ key }}');
const supabaseUrl = 'https://hshcoehesdpiqkewieda.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhzaGNvZWhlc2RwaXFrZXdpZWRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTQyNjkwMTksImV4cCI6MjAwOTg0NTAxOX0.TZmOqR0BItpdkv_WUNtAZa1h99U_XTTgLLbJB1jW_H0'
const supabase = createClient(supabaseUrl, supabaseKey)

console.log('running script.js');

async function updateAvail() {
    console.log('updateAvail script');
    try {
        const { data, error } = await supabase
            .from('rooms')
            .update({ availability: false })
            .eq('roomName', 'Study Room');

        if (error) {
            console.error('Error Update Avail:', error);
        } else {
            console.log('Update Avail:', data);
        }
    } catch (e) {
        console.error('Error updating availability:', e);
    }
  fetch('/book-a-room', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
});
}

async function fetchRooms() {
  console.log('fetchRoom script')
      const { data, error } = await supabase
        .from('rooms')
        .update({ roomName: 'Meeting Hall' })
        .eq('roomName', 'Test Hall')


    if (error) {
        console.error('Error fetching data:', error);
    } else {
        console.log('Fetched data:', data);
    }

}

/* replaced by createSignup() - can delete
async function createEntry() {
  console.log('createEntry script')

  const { data, error } = await supabase
  .from('reservations')
  .insert([
    { id: '1', fName: 'Dylan', lName: 'Edwards', email: 'weebTrash88@aol.com', startTime: '2023-09-09 18:30:00+00', endTime: '2023-09-09 19:30:00+00'},
  ])
  .select()

    if (error) {
        console.error('Error creating: ', error);
    } else {
        console.log('Created Reservation:', data);
    }

}
*/

export async function createSignup(fName,lName,email,startTime,endTime) {
  console.log('createSignup script')

  const { data, error } = await supabase
  .from('reservations')
  .insert([
    { id: '1', fName:fName, lName:lName, email:email, startTime:startTime, endTime:endTime},
  ])
    if (error) {
        console.error('Error creating: ', error);
    } else {
        console.log('Created Reservation:', data);
    }

}

if(!document.getElementById('updateAvailButton')){
  console.log('not bookRoom')
} 
else {
  document.getElementById('updateAvailButton').addEventListener('click', function (e){
    console.log('clicked the update Avail button');
    updateAvail();
  });

  document.getElementById('fetchButton').addEventListener('click', function (e){
    console.log('clicked the Fetch Data button');
    fetchRooms();
  });

  document.getElementById('createDbEntryButton').addEventListener('click', function (e){
    console.log('clicked the Create Entry button');
    createEntry()
  });
}
