document.addEventListener("DOMContentLoaded", () => {
    flatpickr("#date-input", {
        enableTime: true,      // show time picker
        noCalendar: false,     // show calendar
        dateFormat: "m/d D | H:00", // only hour, no minutes
        time_24hr: true,       // 24h format
        minuteIncrement: 60    // step = 1 hour
    });
});