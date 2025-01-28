"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Input } from "@/components/ui/input"

interface VercelOtpInputProps {
  length: number
  onComplete: (otp: string) => void
}

const VercelOtpInput: React.FC<VercelOtpInputProps> = ({ length, onComplete }) => {
  const [otp, setOtp] = useState<string[]>(new Array(length).fill(""))
  const inputRefs = useRef<(HTMLInputElement | null)[]>([])

  useEffect(() => {
    if (inputRefs.current[0]) {
      inputRefs.current[0].focus()
    }
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>, index: number) => {
    const value = e.target.value
    if (isNaN(Number(value))) return

    const newOtp = [...otp]
    newOtp[index] = value.substring(value.length - 1)
    setOtp(newOtp)

    const otpValue = newOtp.join("")
    if (otpValue.length === length) onComplete(otpValue)

    // Move to next input if current field is filled
    if (value && index < length - 1 && inputRefs.current[index + 1]) {
      inputRefs.current[index + 1]?.focus()
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, index: number) => {
    if (e.key === "Backspace" && !otp[index] && index > 0 && inputRefs.current[index - 1]) {
      inputRefs.current[index - 1]?.focus()
    }
  }

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const pastedData = e.clipboardData.getData("text/plain").slice(0, length)
    const newOtp = [...otp]
    for (let i = 0; i < pastedData.length; i++) {
      if (i < length && !isNaN(Number(pastedData[i]))) {
        newOtp[i] = pastedData[i]
      }
    }
    setOtp(newOtp)
    if (newOtp.join("").length === length) {
      onComplete(newOtp.join(""))
    }
    if (inputRefs.current[pastedData.length]) {
      inputRefs.current[pastedData.length]?.focus()
    }
  }

  return (
    <div className="flex justify-between space-x-2">
      {otp.map((digit, index) => (
        <Input
          key={index}
          type="text"
          inputMode="numeric"
          maxLength={1}
          value={digit}
          onChange={(e) => handleChange(e, index)}
          onKeyDown={(e) => handleKeyDown(e, index)}
          onPaste={handlePaste}
          ref={(el) => {
            inputRefs.current[index] = el
          }}
          className="w-10 h-12 text-center text-2xl font-semibold border-2 rounded-md focus:border-blue-500 focus:ring-blue-500"
          style={{ caretColor: "transparent" }}
        />
      ))}
    </div>
  )
}

export default VercelOtpInput