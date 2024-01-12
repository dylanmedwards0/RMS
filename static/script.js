import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import os from "os"

//const supabase = createClient('{{ url }}', '{{ key }}');
const supabaseUrl = os.environ['SUPABASE_URL']
const supabaseKey = os.environ['SUPABASE_KEY']
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

export async function createSignup(fName,lName,email,startTime,endTime) {
  console.log('createSignup script')

// to update - id should be checked against current org id
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

