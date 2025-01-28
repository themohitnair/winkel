import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, BookOpen, ShieldCheck, Users } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="container mx-auto px-4 py-12 md:py-24">
        <header className="text-center mb-16 md:mb-24">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-teal-600">
            Winkel
          </h1>
          <p className="text-xl md:text-2xl text-gray-600">Your College Marketplace</p>
        </header>

        <main className="max-w-4xl mx-auto">
          <section className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-semibold mb-8">Buy. Sell. Connect.</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <FeatureCard
                icon={<BookOpen className="w-8 h-8 text-blue-500" />}
                title="Campus Exclusivity"
                description="Trade within your college community"
              />
              <FeatureCard
                icon={<ShieldCheck className="w-8 h-8 text-blue-500" />}
                title="Secure Transactions"
                description="Safe and verified exchanges"
              />
              <FeatureCard
                icon={<Users className="w-8 h-8 text-blue-500" />}
                title="Student Network"
                description="Connect with peers effortlessly"
              />
            </div>
          </section>

          <section className="bg-white rounded-lg shadow-lg p-8 md:p-12 mb-16 text-center">
            <h2 className="text-2xl md:text-3xl font-semibold mb-6">Ready to dive in?</h2>
            <div className="flex flex-col md:flex-row justify-center space-y-4 md:space-y-0 md:space-x-4">
              <Link href="/auth/signup">
                <Button size="lg" className="w-full md:w-auto group">
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Button>
              </Link>
              <Link href="/auth/login">
                <Button size="lg" variant="outline" className="w-full md:w-auto">
                  Log In
                </Button>
              </Link>
            </div>
          </section>
        </main>

        <footer className="text-center text-gray-500 text-sm">
          <p>&copy; {new Date().getFullYear()} Winkel. All rights reserved.</p>
          <p>Exclusively for college students.</p>
        </footer>
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 transition-all duration-300 hover:shadow-lg">
      <div className="flex justify-center mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}