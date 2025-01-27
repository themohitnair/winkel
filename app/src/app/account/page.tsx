"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import Header from "@/components/Header"

export default function AccountPage() {
  const [fullName, setFullName] = useState("John Doe")
  const [phone, setPhone] = useState("1234567890")
  const [usn, setUsn] = useState("ABC123")
  const [dob, setDob] = useState("1990-01-01")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement account update logic
    console.log("Updating account", {
      fullName,
      phone,
      usn,
      dob,
    })
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Account Details</CardTitle>
            <CardDescription>View and edit your account information.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input id="fullName" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <Input id="phone" type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="usn">USN</Label>
                <Input id="usn" value={usn} onChange={(e) => setUsn(e.target.value)} required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="dob">Date of Birth</Label>
                <Input id="dob" type="date" value={dob} onChange={(e) => setDob(e.target.value)} required />
              </div>
              <Button type="submit" className="w-full">
                Update Account
              </Button>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}

