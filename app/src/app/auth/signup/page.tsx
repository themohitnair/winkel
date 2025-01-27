"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"

export default function SignupPage() {
  const [step, setStep] = useState(1)
  const [phone, setPhone] = useState("")
  const [otp, setOtp] = useState("")
  const [fullName, setFullName] = useState("")
  const [usn, setUsn] = useState("")
  const [dob, setDob] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (step === 1) {
      // TODO: Send OTP to phone number
      setStep(2)
    } else if (step === 2) {
      // TODO: Verify OTP
      setStep(3)
    } else {
      // TODO: Complete signup
      console.log("Signup complete", { phone, fullName, usn, dob })
      router.push("/feed")
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Sign Up</CardTitle>
          <CardDescription>Create your account to start selling or buying.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            {step === 1 && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone Number</Label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="Enter your phone number"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                  />
                </div>
              </div>
            )}
            {step === 2 && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="otp">OTP</Label>
                  <Input
                    id="otp"
                    type="text"
                    placeholder="Enter the OTP"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    required
                  />
                </div>
              </div>
            )}
            {step === 3 && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="fullName">Full Name</Label>
                  <Input
                    id="fullName"
                    type="text"
                    placeholder="Enter your full name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="usn">USN</Label>
                  <Input
                    id="usn"
                    type="text"
                    placeholder="Enter your USN"
                    value={usn}
                    onChange={(e) => setUsn(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="dob">Date of Birth</Label>
                  <Input id="dob" type="date" value={dob} onChange={(e) => setDob(e.target.value)} required />
                </div>
              </div>
            )}
            <Button type="submit" className="w-full mt-4">
              {step === 3 ? "Complete Signup" : "Next"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}