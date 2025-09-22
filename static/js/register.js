const eventRow = document.getElementById('eventRow');
const calendarContainer = document.getElementById('calendarContainer');
const btnCards = document.getElementById('btnCards');
const btnCalendar = document.getElementById('btnCalendar');

btnCards.addEventListener('click', () => {
    eventRow.style.display = 'flex';
    calendarContainer.style.display = 'none';
    btnCards.classList.add('active');
    btnCalendar.classList.remove('active');
});
btnCalendar.addEventListener('click', () => {
    eventRow.style.display = 'none';
    calendarContainer.style.display = 'block';
    btnCalendar.classList.add('active');
    btnCards.classList.remove('active');
});
