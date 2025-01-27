"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { useParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Header from "@/components/Header"
import { Share2 } from "lucide-react"
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel"

interface Listing {
  id: number
  title: string
  price: number
  description: string
  images: string[]
  category: string
  sellerName: string
  sellerPhone: string
  createdAt: string
}

export default function ListingPage() {
  const { id } = useParams()
  const [listing, setListing] = useState<Listing | null>(null)

  useEffect(() => {
    // TODO: Fetch listing data from API
    // This is a mock implementation
    setListing({
      id: Number(id),
      title: "Sample Listing",
      price: 99.99,
      description:
        "This is a detailed description of the listing. It provides more information about the item being sold.",
      images: [
        "/placeholder.svg?text=Image1&width=800&height=600&bg=000000",
        "/placeholder.svg?text=Image2&width=800&height=600&bg=000000",
        "/placeholder.svg?text=Image3&width=800&height=600&bg=000000",
      ],
      category: "Electronics",
      sellerName: "John Doe",
      sellerPhone: "+1234567890",
      createdAt: "2023-06-15T10:30:00Z",
    })
  }, [id])

  if (!listing) {
    return <div>Loading...</div>
  }

  const handleContactSeller = () => {
    window.open(`https://wa.me/${listing.sellerPhone}`, "_blank")
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <Carousel className="w-full max-w-3xl mx-auto">
            <CarouselContent>
              {listing.images.map((image, index) => (
                <CarouselItem key={index}>
                  <div className="p-1">
                    <Image
                      src={image || "/placeholder.svg"}
                      alt={`${listing.title} - Image ${index + 1}`}
                      width={800}
                      height={600}
                      className="w-full h-[300px] md:h-[600px] object-cover rounded-md bg-black"
                    />
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
          <div className="p-4 md:p-6">
            <div className="flex flex-wrap items-start justify-between mb-4">
              <h1 className="text-2xl md:text-3xl font-bold mb-2 md:mb-0">{listing.title}</h1>
              <Badge className="text-sm md:text-lg px-2 py-1">{listing.category}</Badge>
            </div>
            <p className="text-3xl md:text-4xl font-bold text-green-600 mb-4">${listing.price}</p>
            <p className="text-gray-700 mb-6">{listing.description}</p>
            <div className="flex items-center justify-between mb-6">
              <span className="text-sm text-gray-500">Posted by {listing.sellerName}</span>
              <span className="text-sm text-gray-500">{new Date(listing.createdAt).toLocaleDateString()}</span>
            </div>
            <div className="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2">
              <Button onClick={handleContactSeller} className="flex-1">
                Contact via WhatsApp
              </Button>
              <Button variant="outline" className="flex-1">
                <Share2 className="mr-2 h-4 w-4" /> Share
              </Button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}