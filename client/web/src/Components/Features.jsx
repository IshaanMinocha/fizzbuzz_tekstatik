

function Features() {
    return (
        <div id="features-section" className="text-center pt-20 bg-black p-10">
            <h1 className="text-5xl font-semibold  font-thinspaced tracking-widest mb-20 text-white">Prime Features</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-20">
                <div className="bg-white p-6 rounded-md shadow-md mb-10">
                    <h2 className="text-xl font-semibold mb-4">Chrome Extension</h2>
                    <p>Analyzes client-side requests to the backend, fuzzes them to uncover vulnerabilities, and sends findings to a dashboard. It also identifies potential malware threats, enhancing overall security.
                    </p>
                </div>
                <div className="bg-white p-6 rounded-md shadow-md mt-10">
                    <h2 className="text-xl font-semibold mb-4">CLI Tool</h2>
                    <p>Executes thorough server-side scans, logs detected vulnerabilities, and provides customizable fuzzing options for in-depth security analysis. It is designed to find and address potential security weaknesses.
                    </p>
                </div>
                <div className="bg-white p-6 rounded-md shadow-md mb-10">
                    <h2 className="text-xl font-semibold mb-4">IDE Fixer</h2>
                    <p>Offers real-time code issue fixing directly within the IDE, promptly addressing vulnerabilities to minimize exploitation risks. Ensures that only high-quality, secure code is pushed to production.</p>
                </div>
                <div className="bg-white p-6 rounded-md shadow-md mb-10">
                    <h2 className="text-xl font-semibold mb-4">Web/App Dashboard</h2>
                    <p> Centralizes vulnerability data and analytics, presenting detailed risk assessments based on impact and the status of applied fixes. Facilitates comprehensive oversight and management of security issues and solutions.
                    </p>
                </div>
                <div className="bg-white p-6 rounded-md shadow-md mt-10">
                    <h2 className="text-xl font-semibold mb-4">Customizable Test Cases</h2>
                    <p>Enables developers to create fully customizable test cases and payloads. This flexibility ensures the fuzzing process can adapt to unique application structures, improving the accuracy of vulnerability detection.
                    </p>
                </div>
                <div className="bg-white p-6 rounded-md shadow-md mb-10">
                    <h2 className="text-xl font-semibold mb-4">Modular Architecture:</h2>
                    <p>Designed with a modular approach, the platform supports efficient integration with existing tools and workflows. This ensures scalability and ease of maintenance, meeting diverse development needs.
                    </p>
                </div>
            </div>

        </div>
    )
}

export default Features