"use client";

import React, { useState, useEffect } from "react";
import { auth, RecaptchaVerifier } from "@/lib/firebaseClient";
import { signInWithPhoneNumber, ConfirmationResult } from "firebase/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

declare global {
  interface Window {
    recaptchaVerifier: RecaptchaVerifier;
    confirmationResult?: ConfirmationResult;
  }
}

const PhoneAuth: React.FC = () => {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [verificationSent, setVerificationSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined" && auth) {
      if (!window.recaptchaVerifier) {
        window.recaptchaVerifier = new RecaptchaVerifier(auth, "recaptcha-container", {
          size: "invisible",
          callback: () => {
            // reCAPTCHA solved, allow signInWithPhoneNumber.
          },
          "expired-callback": () => {
            setError("reCAPTCHA expired. Please try again.");
          },
        });

        window.recaptchaVerifier.render().then(() => {
          console.log("reCAPTCHA rendered successfully.");
        }).catch(err => {
          console.error("reCAPTCHA rendering failed", err);
        });
      }
    }
  }, []);

  const handleSendCode = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    if (!auth) {
      setError("Authentication is not initialized.");
      setLoading(false);
      return;
    }

    const formattedPhoneNumber = phoneNumber.startsWith('+') ? phoneNumber : `+${phoneNumber}`;
    console.log("Formatted Phone Number:", formattedPhoneNumber); // Log to inspect phone number

    if (!formattedPhoneNumber.match(/^\+[1-9]\d{1,14}$/)) {
      setError("Invalid phone number format. Please use the correct international format (+1234567890).");
      setLoading(false);
      return;
    }

    try {
      const confirmationResult = await signInWithPhoneNumber(auth, formattedPhoneNumber, window.recaptchaVerifier);
      window.confirmationResult = confirmationResult;
      setVerificationSent(true);
    } catch (err) {
      setError("Error sending verification code. Please ensure your phone number is in the correct format (+1234567890).");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyCode = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    if (!window.confirmationResult) {
      setError("Please send verification code first.");
      setLoading(false);
      return;
    }

    try {
      const result = await window.confirmationResult.confirm(verificationCode);
      console.log("Phone authentication successful!", result.user);
      // You can add your post-authentication logic here
    } catch (err) {
      setError("Invalid verification code. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4 max-w-md mx-auto p-4">
      <form onSubmit={handleSendCode} className="space-y-2">
        <Input
          type="tel"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          placeholder="Enter phone number (+1234567890)"
          required
          disabled={loading}
          className="w-full"
        />
        <Button 
          type="submit" 
          disabled={loading || verificationSent}
          className="w-full"
        >
          {loading ? "Sending..." : "Send Verification Code"}
        </Button>
      </form>

      <div id="recaptcha-container"></div>

      {verificationSent && (
        <form onSubmit={handleVerifyCode} className="space-y-2">
          <Input
            type="text"
            value={verificationCode}
            onChange={(e) => setVerificationCode(e.target.value)}
            placeholder="Enter 6-digit verification code"
            required
            disabled={loading}
            className="w-full"
          />
          <Button 
            type="submit" 
            disabled={loading}
            className="w-full"
          >
            {loading ? "Verifying..." : "Verify Code"}
          </Button>
        </form>
      )}

      {error && (
        <p className="text-red-500 text-sm text-center" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

export default PhoneAuth;