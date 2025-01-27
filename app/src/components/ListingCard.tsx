import Image from "next/image"
import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface Listing {
  id: number
  title: string
  price: number
  description: string
  imageUrl: string
  category: string
}

export default function ListingCard({ listing }: { listing: Listing }) {
  return (
    <Link href={`/listing/${listing.id}`}>
      <Card className="hover:shadow-md transition-shadow duration-200">
        <CardContent className="p-3 md:p-4">
          <div className="flex flex-col md:flex-row items-start space-y-4 md:space-y-0 md:space-x-4">
            <div className="w-full md:w-[45%]">
              <Image
                src={listing.imageUrl || `/placeholder.svg?text=${encodeURIComponent(listing.title)}&width=400&height=300&bg=000000`}
                alt={listing.title}
                width={400}
                height={300}
                className="rounded-md object-cover bg-black w-full h-[200px] md:h-[300px]"
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold truncate">{listing.title}</h2>
                <Badge variant="secondary" className="ml-2">
                  {listing.category}
                </Badge>
              </div>
              <p className="text-sm text-gray-500 mt-1 line-clamp-2">{listing.description}</p>
              <div className="flex items-center justify-between mt-2">
                <span className="text-lg font-bold text-green-600">${listing.price}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}