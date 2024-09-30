
function Footer() {
    return (
        <footer className=" text-white shadow bg-black">
            <div className="w-full max-w-screen-xl mx-auto p-4 ">
                <div className="sm:flex sm:items-center sm:justify-between">
                    <a href="#" className="flex items-center mb-4 space-x-3 ">
                        
                        <span className="self-center text-4xl font-semibold whitespace-nowrap dark:text-white">FizzBuzz</span>
                    </a>
                    <ul className="flex flex-wrap items-center mb-6 text-sm font-medium text-gray-500 sm:mb-0 dark:text-gray-400">
                       
                        <li>
                            <a href="#features-section" className="text-2xl hover:underline me-4">Features</a>
                        </li>
                        <li>
                            <a 
                            href="/public/chrome-extension.zip" 
                            className="text-2xl hover:underline me-4"
                            download={'chome-extension.zip'}
                            
                            >Download</a>
                        </li>
                    </ul>
                </div>
                <hr className="my-6 border-gray-200 sm:mx-auto dark:border-gray-700 lg:my-8" />
                <span className="block text-2xl text-gray-500 text-center dark:text-gray-400">Made with 💖 and code by TeKstatik</span>
            </div>
        </footer>


    )
}

export default Footer