import ListingCard from "@/components/ListingCard"
import Header from "@/components/Header"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function FeedPage() {
  // TODO: Fetch listings from API
  const listings = [
    {
      id: 1,
      title: "Calculus Textbook",
      price: 50,
      description: "Slightly used calculus textbook, great condition",
      images: [
        "/placeholder.svg?text=Calculus&width=400&height=300&bg=000000",
        "/placeholder.svg?text=Calculus2&width=400&height=300&bg=000000",
      ],
      category: "Books",
    },
    {
      id: 2,
      title: "MacBook Pro",
      price: 1299,
      description: "Brand new MacBook Pro, still in box",
      images: [
        "/placeholder.svg?text=MacBook&width=400&height=300&bg=000000",
        "/placeholder.svg?text=MacBook2&width=400&height=300&bg=000000",
      ],
      category: "Electronics",
    },
    {
      id: 3,
      title: "Dorm Room Desk",
      price: 75,
      description: "Sturdy desk, perfect for studying",
      images: ["/placeholder.svg?text=Desk&width=400&height=300&bg=000000"],
      category: "Furniture",
    },
    {
      id: 4,
      title: "Physics Lab Manual",
      price: 30,
      description: "Required for PHY201 course",
      images: ["/placeholder.svg?text=Physics&width=400&height=300&bg=000000"],
      category: "Books",
    },
    {
      id: 5,
      title: "Bike",
      price: 150,
      description: "Great for getting around campus",
      images: [
        "/placeholder.svg?text=Bike&width=400&height=300&bg=000000",
        "/placeholder.svg?text=Bike2&width=400&height=300&bg=000000",
      ],
      category: "Transportation",
    },
  ]

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="md:hidden mb-4">
          <Input type="search" placeholder="Search Winkel" className="w-full" />
        </div>
        <div className="grid gap-6 md:gap-8">
          {listings.map((listing) => (
            <ListingCard key={listing.id} listing={{ ...listing, imageUrl: listing.images[0] }} />
          ))}
        </div>
      </main>
      <div className="fixed bottom-4 right-4 md:hidden">
        <Button size="lg" className="rounded-full shadow-lg">
          + Create Listing
        </Button>
      </div>
    </div>
  )
}