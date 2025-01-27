import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-100 to-white">
      <div className="container mx-auto px-4 py-8 md:py-16">
        <header className="text-center mb-8 md:mb-16">
          <h1 className="text-3xl md:text-4xl font-bold mb-2 md:mb-4">Welcome to Winkel</h1>
          <p className="text-lg md:text-xl text-gray-600">Your College-Exclusive Marketplace</p>
        </header>

        <main className="max-w-3xl mx-auto">
          <section className="bg-white rounded-lg shadow-md p-6 md:p-8 mb-8">
            <h2 className="text-xl md:text-2xl font-semibold mb-4">What is Winkel?</h2>
            <p className="text-gray-700 mb-4">
              Winkel is a college-exclusive marketplace where students can buy and sell items within their campus
              community. From textbooks to electronics, furniture to clothing, find everything you need or sell what you
              don&apos;t!
            </p>
            <ul className="list-disc list-inside text-gray-700 mb-4">
              <li>Exclusive to your college</li>
              <li>Safe and secure transactions</li>
              <li>Easy-to-use platform</li>
              <li>Connect with fellow students</li>
            </ul>
          </section>

          <section className="text-center">
            <h2 className="text-xl md:text-2xl font-semibold mb-6">Ready to get started?</h2>
            <div className="flex flex-col md:flex-row justify-center space-y-4 md:space-y-0 md:space-x-4">
              <Link href="/auth/signup" className="w-full md:w-auto">
                <Button size="lg" className="w-full md:w-auto">
                  Sign Up
                </Button>
              </Link>
              <Link href="/auth/login" className="w-full md:w-auto">
                <Button size="lg" variant="outline" className="w-full md:w-auto">
                  Log In
                </Button>
              </Link>
            </div>
          </section>
        </main>

        <footer className="mt-8 md:mt-16 text-center text-gray-600">
          <p>&copy; 2025 Winkel. All rights reserved.</p>
          <p>Winkel is exclusively available to college students.</p>
        </footer>
      </div>
    </div>
  )
}