// --- Configuration ---
const API_ENDPOINT = 'http://127.0.0.1:8000/api/v1/students/risk-assessment';

// --- DOM Element References ---
const studentListContainer = document.getElementById('student-list');
const loadingIndicator = document.getElementById('loading-indicator');
const errorMessage = document.getElementById('error-message');

// --- Helper Functions ---

/**
 * Returns Tailwind CSS classes based on the risk level.
 * @param {string} riskLevel - The risk level ('Low', 'Medium', 'High').
 * @returns {object} - An object with border and background/text classes.
 */
function getRiskStyles(riskLevel) {
    switch (riskLevel) {
        case 'High':
            return {
                border: 'border-red-500',
                badge: 'bg-red-100 text-red-800'
            };
        case 'Medium':
            return {
                border: 'border-amber-500',
                badge: 'bg-amber-100 text-amber-800'
            };
        case 'Low':
            return {
                border: 'border-green-500',
                badge: 'bg-green-100 text-green-800'
            };
        default:
            return {
                border: 'border-slate-300',
                badge: 'bg-slate-100 text-slate-800'
            };
    }
}

/**
 * Creates an HTML card for a single student's risk assessment.
 * @param {object} assessment - The student risk assessment object from the API.
 * @returns {string} - The HTML string for the student card.
 */
function createStudentCard(assessment) {
    const student = assessment.student_details;
    const risk = assessment.predicted_risk;
    const styles = getRiskStyles(risk);

    return `
        <div class="bg-white rounded-xl shadow-md p-6 border-l-4 ${styles.border} transform hover:scale-105 transition-transform duration-300">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-lg font-bold text-slate-800">${student.student_id}</h2>
                <span class="text-sm font-semibold px-3 py-1 rounded-full ${styles.badge}">${risk} Risk</span>
            </div>
            <p class="text-slate-600 text-sm mb-4 h-12">${assessment.justification}</p>
            <div class="grid grid-cols-2 gap-4 text-sm mt-6 pt-4 border-t border-slate-200">
                <div>
                    <p class="text-slate-500 font-medium">Cumulative GPA</p>
                    <p class="font-bold text-xl text-slate-900">${student.cumulative_gpa.toFixed(2)}</p>
                </div>
                <div>
                    <p class="text-slate-500 font-medium">Attendance</p>
                    <p class="font-bold text-xl text-slate-900">${student.attendance_percentage}%</p>
                </div>
            </div>
        </div>
    `;
}

// --- Main Application Logic ---

/**
 * Fetches student data from the API and renders it to the page.
 */
async function fetchAndDisplayStudents() {
    try {
        // Fetch data from the backend API
        const response = await fetch(API_ENDPOINT);

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const assessments = await response.json();

        // Hide loading indicator
        loadingIndicator.classList.add('hidden');

        // Clear any previous content
        studentListContainer.innerHTML = '';

        // Check if there is data to display
        if (assessments.length === 0) {
            studentListContainer.innerHTML = '<p class="text-center text-slate-500 col-span-full">No student data available.</p>';
        } else {
            // Create and append a card for each student
            assessments.forEach(assessment => {
                const cardHTML = createStudentCard(assessment);
                studentListContainer.innerHTML += cardHTML;
            });
        }

    } catch (error) {
        console.error('Failed to fetch student data:', error);
        // Hide loading indicator and show error message
        loadingIndicator.classList.add('hidden');
        errorMessage.classList.remove('hidden');
    }
}

// --- Initial Load ---
// Add an event listener to run the main function when the page content has loaded.
document.addEventListener('DOMContentLoaded', fetchAndDisplayStudents);
