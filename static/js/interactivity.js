// =============================================================================
// TurfSPort — interactivity.js (Flask Edition)
// Image paths: /static/images/...
// Redirect URLs: Flask routes (/, /login, /my-bookings, /venue)
// =============================================================================

// --- Auth Protection ---
// Redirect to /login if user is not logged in (skip on the login page itself)
if (sessionStorage.getItem('isLoggedIn') !== 'true' && !window.location.pathname.endsWith('/login')) {
    window.location.href = '/login';
}

// 1. VENUE DATABASE — image paths now use /static/images/
const venues = {
    'box-cricket': {
        name: 'Greenfield Box Cricket',
        location: '📍 Sector 14, Main Road, City Center',
        desc: 'Welcome to Greenfield Box Cricket, the premier location for 6-a-side matches. Equipped with high-intensity floodlights, professional-grade turf, and dugout areas.',
        images: ['/static/images/box-cricket1.jpg', '/static/images/box-cricket2.jpg', '/static/images/box-cricket3.jpg']
    },
    'pickleball': {
        name: 'Smash Pickleball Court',
        location: '📍 Downtown',
        desc: 'Top quality indoor pickleball courts with synthetic flooring.',
        images: ['/static/images/pickleball1.jpg', '/static/images/pickleball2.jpg', '/static/images/pickleball3.jpg']
    },
    'football': {
        name: 'GoalArena 5v5',
        location: '📍 North City Mall',
        desc: 'High-intensity 5-a-side football turf with floodlights.',
        images: ['/static/images/football1.jpg', '/static/images/football2.jpg', '/static/images/football3.jpg']
    },
    'pool': {
        name: 'Cue Masters Lounge',
        location: '📍 City Center',
        desc: 'Professional 8-ball pool tables in a relaxed lounge setting.',
        images: ['/static/images/pool1.jpg', '/static/images/pool2.jpg', '/static/images/pool3.jpg']
    },
    'bowling': {
        name: 'Strike Zone Alley',
        location: '📍 Westend Mall',
        desc: '10-lane bowling alley with automated scoring and cafe.',
        images: ['/static/images/bowling1.jpg', '/static/images/bowling2.jpg', '/static/images/bowling3.jpg']
    },
    'badminton': {
        name: 'Feather Shuttle Club',
        location: '📍 East End',
        desc: 'Wooden courts designed for professional badminton play.',
        images: ['/static/images/badminton1.jpg', '/static/images/badminton2.jpg', '/static/images/badminton3.jpg']
    },
    'gokarting': {
        name: 'Speedway Tracks',
        location: '📍 Highway 51',
        desc: 'Outdoor 800m go-karting track with professional karts.',
        images: ['/static/images/gokarting1.jpg', '/static/images/gokarting2.jpg', '/static/images/gokarting3.jpg']
    },
    'golf': {
        name: 'Elite Greens Country Club',
        location: '📍 Hillside',
        desc: '18-hole lush green golf course with caddy service.',
        images: ['/static/images/golf1.jpg', '/static/images/golf2.jpg', '/static/images/golf3.jpg']
    },
    'tennis': {
        name: 'Grand Slam Tennis Academy',
        location: '📍 Sports Complex',
        desc: 'Synthetic hard courts for standard tennis matches.',
        images: ['/static/images/tennis1.jpg', '/static/images/tennis2.jpg', '/static/images/tennis3.jpg']
    },
    'volleyball': {
        name: 'Spikers Beach Court',
        location: '📍 Lake View',
        desc: 'Outdoor sand volleyball court by the lake.',
        images: ['/static/images/volleyball1.jpg', '/static/images/volleyball2.jpg', '/static/images/volleyball3.jpg']
    },
    'basketball': {
        name: 'Hoops Indoor Arena',
        location: '📍 Downtown YMCA',
        desc: 'Full-court indoor basketball with hardwood floors.',
        images: ['/static/images/basketball1.jpg', '/static/images/basketball2.jpg', '/static/images/basketball3.jpg']
    },
    'cricket-ground': {
        name: 'Lords Local Ground',
        location: '📍 Outskirts',
        desc: 'Full-size leather ball cricket ground with grass outfield.',
        images: ['/static/images/default1.jpg', '/static/images/default2.jpg', '/static/images/default3.jpg']
    }
};

// 2. MAIN LOGIC
document.addEventListener('DOMContentLoaded', () => {

    // Sync client sessionStorage with server session if present
    try {
        fetch('/api/whoami')
            .then(r => r.json())
            .then(user => {
                if (user && user.email) {
                    try {
                        sessionStorage.setItem('isLoggedIn', 'true');
                        sessionStorage.setItem('currentUser', JSON.stringify({ username: user.username, email: user.email }));
                    } catch (e) { console.warn('whoami: could not write sessionStorage', e); }
                }
            })
            .catch(() => {});
    } catch (e) {}


    // --- E. Navbar Auth Logic ---
    const navLinks = document.querySelector('.navbar-links');
    if (navLinks && sessionStorage.getItem('isLoggedIn') === 'true') {
        const loginLink = Array.from(navLinks.querySelectorAll('a')).find(a => a.getAttribute('href') === '/login');
        if (loginLink) {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                sessionStorage.removeItem('isLoggedIn');
                sessionStorage.removeItem('currentUser');
                window.location.href = '/login';
            });
        }
    }

    // --- A. URL Parameter Logic (venue-detail page) ---
    const urlParams = new URLSearchParams(window.location.search);
    const sportId = urlParams.get('id');

    if (sportId && venues[sportId]) {
        const sportData = venues[sportId];

        const titleEl = document.getElementById('venue-title-display');
        const locEl = document.getElementById('venue-location-display');
        const descEl = document.getElementById('venue-desc-display');

        if (titleEl) titleEl.innerText = sportData.name;
        if (locEl) locEl.innerText = sportData.location;
        if (descEl) descEl.innerText = sportData.desc;

        const img1 = document.getElementById('slider-img-1');
        const img2 = document.getElementById('slider-img-2');
        const img3 = document.getElementById('slider-img-3');

        if (img1 && sportData.images) img1.src = sportData.images[0];
        if (img2 && sportData.images) img2.src = sportData.images[1];
        if (img3 && sportData.images) img3.src = sportData.images[2];
    }

    // --- B. Slider Logic ---
    const slides = document.querySelectorAll('.slider-image');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const dots = document.querySelectorAll('.slider-dot');
    let currentSlide = 0;

    function showSlide(index) {
        if (!slides.length) return;
        if (index >= slides.length) { currentSlide = 0; }
        else if (index < 0) { currentSlide = slides.length - 1; }
        else { currentSlide = index; }
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        slides[currentSlide].classList.add('active');
        if (dots[currentSlide]) dots[currentSlide].classList.add('active');
    }

    if (prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
        nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));
    }
    dots.forEach((dot, index) => dot.addEventListener('click', () => showSlide(index)));

    // --- C. Booking Form Validation & API ---
    const bookingForm = document.getElementById('booking-form');
    const dateInput = document.getElementById('booking-date');
    const timeInput = document.getElementById('booking-time');
    const slotsContainer = document.getElementById('slots-container');

    if (dateInput && slotsContainer) {
        dateInput.addEventListener('change', async function() {
            const dateStr = this.value;
            const venueName = document.getElementById('venue-title-display') ? document.getElementById('venue-title-display').innerText : '';
            if (!dateStr || !venueName) return;
            
            slotsContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 14px; grid-column: 1 / -1;">Loading slots...</p>';
            if(timeInput) timeInput.value = ''; 
            
            try {
                const response = await fetch(`/api/slots?venue_name=${encodeURIComponent(venueName)}&date=${dateStr}`);
                const slots = await response.json();
                console.debug('api/slots response', slots);
                
                if (slots.error) {
                    slotsContainer.innerHTML = `<p style="color: var(--error); font-size: 14px; grid-column: 1 / -1;">${slots.error}</p>`;
                    return;
                }
                
                slotsContainer.innerHTML = '';
                if (slots.length === 0) {
                    slotsContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 14px; grid-column: 1 / -1;">No slots available for this venue (API returned 0 slots).</p>';
                }
                
                slots.forEach(slot => {
                    const chip = document.createElement('div');
                    chip.className = 'slot-chip' + (slot.is_booked ? ' booked' : '');
                    chip.textContent = slot.display_time;
                    if (!slot.is_booked) {
                        chip.addEventListener('click', () => {
                            document.querySelectorAll('.slot-chip').forEach(c => c.classList.remove('selected'));
                            chip.classList.add('selected');
                            if(timeInput) timeInput.value = slot.id; // Store slot_id
                            const errDiv = document.getElementById('booking-time-error');
                            if(errDiv) errDiv.style.display = 'none';
                        });
                    }
                    slotsContainer.appendChild(chip);
                });
            } catch (err) {
                slotsContainer.innerHTML = '<p style="color: var(--error); font-size: 14px; grid-column: 1 / -1;">Failed to load slots.</p>';
            }
        });
    }

    function clearErrors() {
        document.querySelectorAll('.error-message').forEach(msg => msg.style.display = 'none');
        document.querySelectorAll('.input-error').forEach(input => input.classList.remove('input-error'));
    }

    function showError(inputId, message) {
        const inputElement = document.getElementById(inputId);
        const errorDiv = document.getElementById(inputId + '-error');
        if (errorDiv) { errorDiv.textContent = message; errorDiv.style.display = 'block'; }
        if (inputElement) inputElement.classList.add('input-error');
    }

    if (bookingForm) {
        bookingForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            clearErrors();
            let isValid = true;

            const nameInput = document.getElementById('customer-name');
            if (!nameInput || nameInput.value.trim() === '') { showError('customer-name', 'Name is required.'); isValid = false; }

            const phoneInput = document.getElementById('customer-phone');
            const phoneRegex = /^[0-9]{10}$/;
            if (!phoneInput || !phoneRegex.test(phoneInput.value.trim())) { showError('customer-phone', 'Please enter a valid 10-digit phone number.'); isValid = false; }

            const dateInput = document.getElementById('booking-date');
            if (dateInput && dateInput.value) {
                const selectedDate = new Date(dateInput.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                if (selectedDate < today) { showError('booking-date', 'Booking date cannot be in the past.'); isValid = false; }
            } else { showError('booking-date', 'Please select a date.'); isValid = false; }

            const timeInput = document.getElementById('booking-time');
            if (!timeInput || timeInput.value === '') { showError('booking-time', 'Please select a time slot.'); isValid = false; }

            if (isValid) {
                const bookingDate = dateInput.value;
                const slotId = timeInput.value;
                const venueName = document.getElementById('venue-title-display') ? document.getElementById('venue-title-display').innerText : 'Selected Venue';

                const currentUserStr = sessionStorage.getItem('currentUser');
                const currentUser = currentUserStr ? JSON.parse(currentUserStr) : { username: 'testuser' };
                const userEmail = currentUser.email || currentUser.username || '';
                
                try {
                    const response = await fetch('/book', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            venue_name: venueName,
                            slot_id: slotId,
                            date: bookingDate,
                            email: userEmail,
                            username: currentUser.username
                        })
                    });
                    
                    const result = await response.json();
                    if (response.ok) {
                        alert('Booking Confirmed!');
                        window.location.href = '/my-bookings';
                    } else {
                        alert(result.error || 'Failed to book slot.');
                        dateInput.dispatchEvent(new Event('change')); // Refresh slots
                    }
                } catch (err) {
                    alert('Error communicating with server.');
                }
            }
        });
    }

    // --- D. My Bookings Logic ---
    const dynamicBookings = document.getElementById('dynamic-bookings');
    if (dynamicBookings) {
        dynamicBookings.innerHTML = '<p style="color: var(--text-muted); margin-bottom: 24px;">Loading bookings...</p>';
        const currentUserStr = sessionStorage.getItem('currentUser');
        const currentUser = currentUserStr ? JSON.parse(currentUserStr) : { username: 'testuser' };
        const userEmail = currentUser.email || currentUser.username || '';
        const bookingsUrl = userEmail ? `/api/my-bookings?email=${encodeURIComponent(userEmail)}` : '/api/my-bookings';

        fetch(bookingsUrl)
            .then(res => res.json())
            .then(bookings => {
                if (bookings.length === 0) {
                    dynamicBookings.innerHTML = '<p style="color: var(--text-muted); margin-bottom: 24px;">You have no bookings yet.</p>';
                } else {
                    dynamicBookings.innerHTML = '';
                    bookings.forEach(booking => {
                        const dateObj = new Date(booking.date);
                        const formattedDate = dateObj.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
                        
                        let cancelBtn = '';
                        let badgeClass = booking.status === 'Confirmed' ? 'status-confirmed' : 'status-past';
                        if (booking.status === 'Confirmed') {
                            cancelBtn = `<button class="btn-cancel" onclick="cancelBooking(${booking.id})">Cancel Booking</button>`;
                        }

                        const card = document.createElement('div');
                        card.className = 'booking-card';
                        card.id = `booking-${booking.id}`;
                        card.innerHTML = `
                            <div class="booking-details">
                                <h3>${booking.venueName}</h3>
                                <p><strong>Sport:</strong> ${booking.sport}</p>
                                <p><strong>Date:</strong> ${formattedDate !== 'Invalid Date' ? formattedDate : booking.date}</p>
                                <p><strong>Time:</strong> ${booking.time}</p>
                                <p><strong>Price:</strong> ${booking.price}</p>
                            </div>
                            <div class="booking-status">
                                <span class="status-badge ${badgeClass}">${booking.status}</span><br>
                                ${cancelBtn}
                            </div>
                        `;
                        dynamicBookings.appendChild(card);
                    });
                }
            })
            .catch(err => {
                dynamicBookings.innerHTML = '<p style="color: var(--error); margin-bottom: 24px;">Failed to load bookings.</p>';
            });
    }
});

// Cancel booking (global scope so onclick can call it)
window.cancelBooking = async function (id) {
    if (confirm('Are you sure you want to cancel this booking?')) {
        try {
            const response = await fetch(`/cancel-booking/${id}`, { method: 'POST' });
            if (response.ok) {
                const bookingCard = document.getElementById(`booking-${id}`);
                if (bookingCard) {
                    const badge = bookingCard.querySelector('.status-badge');
                    if (badge) {
                        badge.textContent = 'CANCELLED';
                        badge.className = 'status-badge status-past';
                    }
                    const btn = bookingCard.querySelector('.btn-cancel');
                    if (btn) btn.remove();
                }
            } else {
                alert('Failed to cancel booking.');
            }
        } catch (err) {
            alert('Error cancelling booking.');
        }
    }
};

// --- E. Analytics Dashboard Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('analyticsChartCanvas');
    if (!canvas) return; // Only run on analytics page

    let currentChart = null;
    let currentData = null;
    let currentView = 'trend'; // 'trend', 'revenue', 'peak'

    const monthSelect = document.getElementById('filter-month');
    const yearSelect = document.getElementById('filter-year');
    const resetZoomBtn = document.getElementById('reset-zoom-btn');
    const tabs = document.querySelectorAll('.chart-tab');
    
    // Load filters
    async function loadFilters() {
        try {
            const res = await fetch('/api/analytics/filters');
            const data = await res.json();
            
            if (yearSelect) {
                yearSelect.innerHTML = data.years.map(y => `<option value="${y}">${y}</option>`).join('');
                if (data.years.length > 0) yearSelect.value = data.years[0];
            }
            if (monthSelect) {
                monthSelect.innerHTML = data.months.map(m => `<option value="${m.value}">${m.label}</option>`).join('');
                monthSelect.value = ""; 
            }
        } catch (e) {
            console.error("Error loading filters", e);
        }
    }

    async function loadAnalyticsData() {
        const month = monthSelect ? monthSelect.value : '';
        const year = yearSelect ? yearSelect.value : '';
        
        let url = '/api/analytics?';
        if (month) url += `month=${month}&`;
        if (year) url += `year=${year}`;
        
        try {
            const res = await fetch(url);
            const data = await res.json();
            
            // Update summary cards
            const setText = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
            setText('total-bookings', data.summary.total_bookings);
            setText('confirmed-bookings', data.summary.confirmed_bookings);
            setText('cancelled-bookings', data.summary.cancelled_bookings);
            setText('revenue', `₹${data.summary.revenue.toLocaleString()}`);
            setText('average-booking', `₹${data.summary.average_booking_value.toLocaleString()}`);
            setText('top-venue', data.summary.top_venue || '-');
            setText('busiest-day', `Peak day: ${data.summary.busiest_day || '-'}`);
            
            currentData = data;
            renderChart();
        } catch(e) {
            console.error("Error loading analytics data", e);
        }
    }
    
    function renderChart() {
        if (!currentData) return;
        
        if (currentChart) {
            currentChart.destroy();
        }
        
        const ctx = canvas.getContext('2d');
        let config = {};
        
        if (currentView === 'trend') {
            const labels = currentData.trend_series.map(d => d.date);
            const bookings = currentData.trend_series.map(d => d.bookings);
            const revenues = currentData.trend_series.map(d => d.revenue);
            
            config = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Bookings',
                            data: bookings,
                            borderColor: '#059669',
                            backgroundColor: '#059669',
                            yAxisID: 'y'
                        },
                        {
                            label: 'Revenue (₹)',
                            data: revenues,
                            type: 'bar',
                            backgroundColor: 'rgba(147, 51, 234, 0.5)',
                            borderColor: '#9333EA',
                            borderWidth: 1,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    scales: {
                        y: { type: 'linear', display: true, position: 'left', title: {display: true, text: 'Bookings'}, beginAtZero: true },
                        y1: { type: 'linear', display: true, position: 'right', grid: {drawOnChartArea: false}, title: {display: true, text: 'Revenue (₹)'}, beginAtZero: true }
                    },
                    plugins: {
                        zoom: {
                            pan: {
                                enabled: true,
                                mode: 'x'
                            },
                            zoom: {
                                wheel: { enabled: true },
                                pinch: { enabled: true },
                                mode: 'x'
                            }
                        }
                    }
                }
            };
            const subtitle = document.getElementById('chart-subtitle');
            if(subtitle) subtitle.textContent = 'Displays confirmed bookings and revenue per day to help you track volume trends.';
        } else if (currentView === 'revenue') {
            const labels = currentData.revenue_by_sport.map(d => d.label);
            const values = currentData.revenue_by_sport.map(d => d.value);
            
            config = {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: ['#4338CA', '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#14B8A6', '#F97316', '#6366F1', '#84CC16']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        zoom: { pan: {enabled: false}, zoom: {wheel: {enabled: false}, pinch: {enabled:false}} }
                    }
                }
            };
            const subtitle = document.getElementById('chart-subtitle');
            if(subtitle) subtitle.textContent = 'Displays revenue distribution among the different sports.';
        } else if (currentView === 'peak') {
            const labels = currentData.peak_times.map(d => d.label);
            const values = currentData.peak_times.map(d => d.value);
            
            config = {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Total Bookings',
                        data: values,
                        backgroundColor: '#3B82F6',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    },
                    plugins: {
                        zoom: { pan: {enabled: false}, zoom: {wheel: {enabled: false}, pinch: {enabled:false}} }
                    }
                }
            };
            const subtitle = document.getElementById('chart-subtitle');
            if(subtitle) subtitle.textContent = 'Displays the most popular days of the week.';
        }
        
        currentChart = new Chart(ctx, config);
    }
    
    if (monthSelect) monthSelect.addEventListener('change', loadAnalyticsData);
    if (yearSelect) yearSelect.addEventListener('change', loadAnalyticsData);
    
    if (resetZoomBtn) {
        resetZoomBtn.addEventListener('click', () => {
            if (currentChart && currentView === 'trend') {
                currentChart.resetZoom();
            }
        });
    }
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentView = tab.dataset.view;
            renderChart();
        });
    });
    
    // Init
    loadFilters().then(() => loadAnalyticsData());
});
