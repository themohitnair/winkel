import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Menu, Search, Plus } from 'lucide-react'
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet"

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200">
      <div className="container mx-auto px-4 py-2 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="md:hidden">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left">
              <nav className="flex flex-col space-y-4 mt-4">
                <Link href="/feed" className="text-lg font-medium">
                  Feed
                </Link>
                <Link href="/account" className="text-lg font-medium">
                  Account
                </Link>
                <Link href="/auth/login" className="text-lg font-medium">
                  Log Out
                </Link>
              </nav>
            </SheetContent>
          </Sheet>
          <Link href="/feed" className="text-2xl font-bold">
            Winkel
          </Link>
        </div>
        <div className="hidden md:flex flex-1 max-w-md mx-4">
          <Input type="search" placeholder="Search Winkel" className="w-full" />
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon" className="md:hidden">
            <Search className="h-5 w-5" />
          </Button>
          <Link href="/create-listing">
            <Button size="sm" className="hidden md:flex">
              Create Listing
            </Button>
            <Button variant="ghost" size="icon" className="md:hidden">
              <Plus className="h-5 w-5" />
            </Button>
          </Link>
          <nav className="hidden md:flex space-x-2">
            <Link href="/feed">
              <Button variant="ghost" size="sm">Feed</Button>
            </Link>
            <Link href="/account">
              <Button variant="ghost" size="sm">Account</Button>
            </Link>
            <Link href="/auth/login">
              <Button size="sm">Log Out</Button>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}