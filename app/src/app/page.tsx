import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowRight, BookOpen, DollarSign, Users, Menu, Shield } from "lucide-react"
import { Dialog, DialogContent, DialogTrigger, DialogTitle } from "@/components/ui/dialog"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center border-b">
        <Link className="flex items-center justify-center" href="#">
          <BookOpen className="h-6 w-6 mr-2" />
          <span className="font-bold">winkel</span>
        </Link>
        <nav className="ml-auto hidden md:flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline underline-offset-4" href="https://github.com/themohitnair/winkel/blob/main/README.md">
            About
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4" href="https://github.com/themohitnair/winkel">
            Source Code
          </Link>
          
        </nav>
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="md:hidden">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="right">
            <nav className="flex flex-col gap-4">
              <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
                Features
              </Link>
              <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
                About
              </Link>
              <Link className="text-sm font-medium hover:underline underline-offset-4" href="#">
                Contact
              </Link>
            </nav>
          </SheetContent>
        </Sheet>
      </header>
      <main className="flex-1 flex flex-col lg:flex-row">
        <div className="flex-1 flex flex-col justify-center px-4 py-8 md:px-6 lg:py-12">
          <div className="space-y-2 mb-4">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
              Your Campus Marketplace
            </h1>
            <p className="text-xl text-gray-500 dark:text-gray-400 max-w-[600px]">
              Buy, sell, and trade with your fellow students.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4">
            <Button asChild size="lg">
              <Link href="/signup">Sign Up</Link>
            </Button>
            <Button variant="outline" asChild size="lg">
              <Link href="/login">Log In</Link>
            </Button>
          </div>
        </div>
        <div className="flex-1 flex items-center justify-center bg-gray-100 dark:bg-gray-800 p-4 lg:p-8">
          <div className="space-y-8 w-full max-w-md">
            {[
              {
                icon: Users,
                color: "text-blue-500",
                title: "Connect with Peers",
                description: "Buy and sell with students on campus.",
              },
              {
                icon: DollarSign,
                color: "text-green-500",
                title: "Save Money",
                description: "Find deals on books and more.",
              },
              {
                icon: ArrowRight,
                color: "text-purple-500",
                title: "Easy to Use",
                description: "Simple interface for quick transactions.",
              },
              {
                icon: Shield,
                color: "text-red-500",
                title: "Data Safety",
                description: "Foolproof Authentication",
              },
            ].map((feature, index) => (
              <div key={index} className="flex items-center space-x-4">
                <feature.icon className={`h-10 w-10 ${feature.color}`} />
                <div>
                  <h3 className="font-bold">{feature.title}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{feature.description}</p>
                </div>
              </div>
            ))}
            <div className="flex justify-center pt-4">
              <Button size="lg" asChild>
                <Link href="/signup">
                  Get Started <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </main>
      <footer className="flex flex-col sm:flex-row justify-between items-center px-4 py-6 border-t text-sm">
        <p className="text-gray-500 dark:text-gray-400 mb-4 sm:mb-0">© 2025 winkel</p>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="link" className="p-0 h-auto">
              Terms of Service
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogTitle>Terms of Service (Condensed)</DialogTitle>
            <ul className="list-disc pl-5 space-y-2 text-sm text-gray-500">
              <li>By using winkel, you agree to our terms.</li>
              <li>We provide a platform for college students to buy and sell items.</li>
              <li>Users are responsible for their transactions.</li>
              <li>We do not guarantee any sales or purchases.</li>
              <li>Prohibited items include illegal goods, weapons, and explicit content.</li>
              <li>We reserve the right to remove any listing or user account that violates these terms.</li>
              <li>
                For a more detailed ToS: visit{" "}
                <Link className="text-blue-500 hover:underline" href="#">
                  winkel ToS
                </Link>
              </li>
            </ul>
          </DialogContent>
        </Dialog>
      </footer>
    </div>
  )
}