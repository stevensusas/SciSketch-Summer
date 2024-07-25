import React from 'react';
import { Link } from 'react-router-dom';

const Landing = () => {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <header className="bg-white shadow-md sticky top-0 z-50 w-full">
                <div className="container mx-auto px-8 py-6 flex justify-between items-center">
                    <Link to="/">
                        <h1 className="text-4xl font-bold text-blue-600">SciSketch</h1>
                    </Link>
                    <nav>
                        <Link to="/page1" className="text-gray-800 hover:text-blue-600 transition duration-300 mr-4">Page 1</Link>
                        <Link to="/page2" className="text-gray-800 hover:text-blue-600 transition duration-300 mr-4">Page 2</Link>
                        <Link to="/login?mode=signup">
                            <button className="bg-blue-500 text-white rounded-full px-4 py-2 mr-2 hover:bg-blue-600 transition duration-300">Sign Up</button>
                        </Link>
                        <Link to="/login?mode=login">
                            <button className="bg-transparent border border-blue-500 text-blue-500 rounded-full px-4 py-2 hover:bg-blue-500 hover:text-white transition duration-300">Log In</button>
                        </Link>
                    </nav>
                </div>
            </header>

            <main className="flex-grow container mx-auto px-8">
                <section className="relative text-center mb-12 py-44 -mx-32">
                    <video autoPlay loop muted className="absolute inset-0 w-full h-full object-cover z-0">
                        <source src="https://videos.pexels.com/video-files/3191572/3191572-uhd_2560_1440_25fps.mp4" type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                    <div className="absolute inset-0 bg-blue-500 opacity-50 z-0"></div>
                    <div className="relative z-10">
                        <h2 className="text-6xl font-bold text-white mb-12">Welcome to SciSketch</h2>
                        <p className="text-xl text-white">AI-powered editing and illustration for scientists.</p>
                    </div>
                </section>

                <section className="mb-24">
                    <h3 className="text-3xl font-bold text-gray-800 mb-16 text-center">Why Choose SciSketch?</h3>
                    <div className="flex flex-col md:flex-row md:space-x-16 space-y-16 md:space-y-0">
                        <div className="bg-white shadow-lg rounded-lg p-12 flex-1 text-center">
                            <h4 className="text-2xl font-bold text-blue-600 mb-6">Productivity</h4>
                            <p className="text-gray-600">Boost your productivity with AI.</p>
                        </div>
                        <div className="bg-white shadow-lg rounded-lg p-12 flex-1 text-center">
                            <h4 className="text-2xl font-bold text-blue-600 mb-6">Accuracy</h4>
                            <p className="text-gray-600">Ensure accuracy and consistency.</p>
                        </div>
                        <div className="bg-white shadow-lg rounded-lg p-12 flex-1 text-center">
                            <h4 className="text-2xl font-bold text-blue-600 mb-6">User-Friendly</h4>
                            <p className="text-gray-600">Easy to use interface.</p>
                        </div>
                    </div>
                </section>

                <section className="mb-24">
                    <h3 className="text-3xl font-bold text-gray-800 mb-16 text-center">Testimonials</h3>
                    <div className="space-y-16">
                        <div className="bg-white shadow-lg rounded-lg p-12 text-center">
                            <p className="text-gray-600 mb-6">"SciSketch is incredibly accurate and easy to use."</p>
                            <p className="text-blue-600 font-bold">- Dr. Jane Smith</p>
                        </div>
                        <div className="bg-white shadow-lg rounded-lg p-12 text-center">
                            <p className="text-gray-600 mb-6">"Creating diagrams has never been easier."</p>
                            <p className="text-blue-600 font-bold">- Prof. John Doe</p>
                        </div>
                    </div>
                </section>
            </main>

            <footer className="bg-gray-200 py-10">
                <div className="container mx-auto px-8">
                    <p className="text-center text-gray-600">© 2024 SciSketch. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default Landing;
