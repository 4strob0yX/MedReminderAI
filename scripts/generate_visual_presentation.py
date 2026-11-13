#!/usr/bin/env python3
"""
Generates the 15-slide visual presentation (ZERO letters/text on slides) for the
MedReminder AI Infographic:
  - 15 Full HD (1920x1080, 16:9) slides, one per number (1..15)
  - Outputs:
      1. MedReminderAI_Presentacion_15_Numeros.pptx (PowerPoint 16:9 with speaker notes)
      2. MedReminderAI_Presentacion_15_Numeros.pdf  (Full HD 16:9 PDF deck)
      3. MedReminderAI_Presentacion_Interactiva.html (Interactive HTML5 presentation)
"""

import os
import shutil
import subprocess
import zipfile
from xml.sax.saxutils import escape
from PIL import Image

OUT_DIR_DEV = "/Users/4strob0y/Developer/MedReminderAI/docs"
OUT_DIR_DL = "/Users/4strob0y/Downloads/MedReminderAI/docs"
SCRATCH_DIR = "/Users/4strob0y/.gemini/antigravity/brain/df7f6cea-1270-4cf2-93ec-9cc9422b334c/scratch/slides_build"
ARTIFACT_DIR = "/Users/4strob0y/.gemini/antigravity/brain/df7f6cea-1270-4cf2-93ec-9cc9422b334c"

os.makedirs(SCRATCH_DIR, exist_ok=True)
os.makedirs(OUT_DIR_DEV, exist_ok=True)

# Exact 15 sentences from the infographic (only used for PowerPoint speaker notes & secret study mode)
SLIDES_META = [
    # Section 1: EASY TO USE (Teal / Blue)
    {
        "num": 1,
        "section": 1,
        "badge_color": "#2B88D8",
        "card_bg": "#E3F4FC",
        "blob_color": "#C9E8FA",
        "accent_glow": "#0EA5E9",
        "sentence": "Users are registered in the application.",
        "verb_focus": "are registered",
    },
    {
        "num": 2,
        "section": 1,
        "badge_color": "#2B88D8",
        "card_bg": "#E3F4FC",
        "blob_color": "#C9E8FA",
        "accent_glow": "#0284C7",
        "sentence": "Everything is kept simple with large buttons.",
        "verb_focus": "is kept simple",
    },
    {
        "num": 3,
        "section": 1,
        "badge_color": "#2B88D8",
        "card_bg": "#E3F4FC",
        "blob_color": "#C9E8FA",
        "accent_glow": "#06B6D4",
        "sentence": "Voice commands are used instead of typing.",
        "verb_focus": "are used",
    },
    {
        "num": 4,
        "section": 1,
        "badge_color": "#2B88D8",
        "card_bg": "#E3F4FC",
        "blob_color": "#C9E8FA",
        "accent_glow": "#0284C7",
        "sentence": "The setup is completed in just two minutes.",
        "verb_focus": "is completed",
    },
    {
        "num": 5,
        "section": 1,
        "badge_color": "#2B88D8",
        "card_bg": "#E3F4FC",
        "blob_color": "#C9E8FA",
        "accent_glow": "#14B8A6",
        "sentence": "Clear text is provided to make reading easier.",
        "verb_focus": "is provided",
    },
    # Section 2: SMART & SECURE (Orange / Coral / Amber)
    {
        "num": 6,
        "section": 2,
        "badge_color": "#DC4C64",
        "card_bg": "#FDECE6",
        "blob_color": "#FBD5C8",
        "accent_glow": "#E11D48",
        "sentence": "Your data is kept encrypted.",
        "verb_focus": "is kept encrypted",
    },
    {
        "num": 7,
        "section": 2,
        "badge_color": "#DC4C64",
        "card_bg": "#FDECE6",
        "blob_color": "#FBD5C8",
        "accent_glow": "#F43F5E",
        "sentence": "Alerts are sent to you at the right time.",
        "verb_focus": "are sent",
    },
    {
        "num": 8,
        "section": 2,
        "badge_color": "#E07A2A",
        "card_bg": "#FEF0DF",
        "blob_color": "#FDE0BC",
        "accent_glow": "#EA580C",
        "sentence": "Your medication routine is learned by AI.",
        "verb_focus": "is learned",
    },
    {
        "num": 9,
        "section": 2,
        "badge_color": "#E07A2A",
        "card_bg": "#FEF0DF",
        "blob_color": "#FDE0BC",
        "accent_glow": "#D97706",
        "sentence": "You can control who is allowed to see your data.",
        "verb_focus": "is allowed",
    },
    {
        "num": 10,
        "section": 2,
        "badge_color": "#E58E26",
        "card_bg": "#FEF0DF",
        "blob_color": "#FDE0BC",
        "accent_glow": "#F59E0B",
        "sentence": "Refill alerts are sent to prevent shortages.",
        "verb_focus": "are sent",
    },
    # Section 3: ALWAYS CONNECTED (Purple / Teal / Rose)
    {
        "num": 11,
        "section": 3,
        "badge_color": "#3898EC",
        "card_bg": "#E6F4FC",
        "blob_color": "#CCE8FA",
        "accent_glow": "#6366F1",
        "sentence": "Your family is added to your care circle.",
        "verb_focus": "is added",
    },
    {
        "num": 12,
        "section": 3,
        "badge_color": "#E04F70",
        "card_bg": "#FCECF0",
        "blob_color": "#F9D5DF",
        "accent_glow": "#EC4899",
        "sentence": "Missed-dose alerts are received by caregivers.",
        "verb_focus": "are received",
    },
    {
        "num": 13,
        "section": 3,
        "badge_color": "#26A688",
        "card_bg": "#E4F8F2",
        "blob_color": "#C6F0E3",
        "accent_glow": "#10B981",
        "sentence": "Progress reports are automatically generated.",
        "verb_focus": "are automatically generated",
    },
    {
        "num": 14,
        "section": 3,
        "badge_color": "#F0982B",
        "card_bg": "#FEF3E2",
        "blob_color": "#FDE4BD",
        "accent_glow": "#F59E0B",
        "sentence": "Distance is bridged by connectivity.",
        "verb_focus": "is bridged",
    },
    {
        "num": 15,
        "section": 3,
        "badge_color": "#6328A8",
        "card_bg": "#F4EBFC",
        "blob_color": "#E6D2F9",
        "accent_glow": "#8B5CF6",
        "sentence": "Healthy habits are supported by AI.",
        "verb_focus": "are supported",
    },
]

# High-detail custom SVGs matching each of the 15 infographic illustrations (ZERO letters)
SVG_ILLUSTRATIONS = {
    1: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft organic background blob -->
      <path d="M95 140 C160 65, 350 65, 410 150 C465 230, 445 370, 365 425 C285 480, 140 465, 85 385 C35 310, 40 205, 95 140 Z" fill="#CBEAFB"/>
      <!-- Registration Profile Card -->
      <g filter="url(#dropShadow)">
        <rect x="95" y="65" width="285" height="365" rx="26" fill="#FFFFFF" stroke="#1E293B" stroke-width="6"/>
        <!-- Subtle top card highlight -->
        <path d="M121 72 H354" stroke="#E2E8F0" stroke-width="4" stroke-linecap="round"/>
      </g>
      <!-- Avatar Circle Backdrop -->
      <circle cx="237" cy="198" r="88" fill="#D2E8F8"/>
      <!-- Clip for Avatar Shoulders inside Circle -->
      <clipPath id="avatarClip1">
        <circle cx="237" cy="198" r="88"/>
      </clipPath>
      <g clip-path="url(#avatarClip1)">
        <!-- Blue Shirt / Shoulders -->
        <path d="M150 295 C155 245, 190 232, 237 232 C284 232, 319 245, 324 295 Z" fill="#2E90E8" stroke="#1E293B" stroke-width="5.5" stroke-linejoin="round"/>
        <!-- Shirt Collar / Shading -->
        <path d="M210 233 Q237 255 264 233" fill="#F6B092" stroke="#1E293B" stroke-width="5"/>
        <!-- Neck -->
        <rect x="220" y="205" width="34" height="34" rx="10" fill="#F6B092" stroke="#1E293B" stroke-width="5"/>
        <!-- Ears -->
        <circle cx="195" cy="176" r="11" fill="#F6B092" stroke="#1E293B" stroke-width="5"/>
        <circle cx="279" cy="176" r="11" fill="#F6B092" stroke="#1E293B" stroke-width="5"/>
        <!-- Head -->
        <path d="M196 155 C196 125, 278 125, 278 155 C278 195, 262 216, 237 216 C212 216, 196 195, 196 155 Z" fill="#FBC2A6" stroke="#1E293B" stroke-width="5.5"/>
        <!-- Hair -->
        <path d="M193 166 C188 135, 205 112, 238 113 C262 113, 272 122, 279 130 C287 139, 285 156, 280 166 C277 150, 268 142, 252 142 C230 142, 212 138, 200 152 Z" fill="#263849" stroke="#1E293B" stroke-width="5" stroke-linejoin="round"/>
      </g>
      <circle cx="237" cy="198" r="88" stroke="#BDDDF4" stroke-width="4" fill="none"/>
      <!-- Clean Graphic UI Lines (No letters) -->
      <rect x="135" y="318" width="185" height="20" rx="10" fill="#CEE5F6"/>
      <rect x="135" y="354" width="142" height="20" rx="10" fill="#CEE5F6"/>
      <!-- Green Checkmark Badge -->
      <g filter="url(#dropShadow)">
        <circle cx="372" cy="366" r="54" fill="#32B67A" stroke="#1E293B" stroke-width="6"/>
        <path d="M346 366 L364 384 L399 348" stroke="#FFFFFF" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </svg>
    """,

    2: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Background Blob -->
      <ellipse cx="250" cy="265" rx="185" ry="165" fill="#CBEAFB"/>
      <!-- Tilted Smartphone with 4 Large Buttons -->
      <g transform="rotate(-5 250 255)" filter="url(#dropShadow)">
        <!-- Phone Outer Body -->
        <rect x="115" y="45" width="270" height="430" rx="36" fill="#243447" stroke="#1E293B" stroke-width="6"/>
        <!-- Inner Screen -->
        <rect x="131" y="68" width="238" height="384" rx="22" fill="#FFFFFF" stroke="#1E293B" stroke-width="4"/>
        <!-- Speaker Notch -->
        <rect x="215" y="55" width="70" height="7" rx="3.5" fill="#0F172A"/>
        <!-- Button 1: Top-Left Blue (Pill Icon) -->
        <rect x="148" y="102" width="94" height="94" rx="18" fill="#3B82F6" stroke="#2563EB" stroke-width="3"/>
        <g transform="rotate(-40 195 149)">
          <rect x="177" y="121" width="36" height="56" rx="18" fill="#FFFFFF" stroke="#1E3A8A" stroke-width="3"/>
          <path d="M177 149 H213 V159 A18 18 0 0 1 177 159 Z" fill="#93C5FD"/>
          <line x1="177" y1="149" x2="213" y2="149" stroke="#1E3A8A" stroke-width="3"/>
        </g>
        <!-- Button 2: Top-Right Orange/Amber (Bell Icon) -->
        <rect x="258" y="102" width="94" height="94" rx="18" fill="#F59E0B" stroke="#D97706" stroke-width="3"/>
        <path d="M305 123 C292 123, 284 133, 284 147 V160 L277 167 H333 L326 160 V147 C326 133, 318 123, 305 123 Z" fill="#FFFFFF"/>
        <circle cx="305" cy="173" r="6" fill="#FFFFFF"/>
        <circle cx="305" cy="120" r="4" fill="#FFFFFF"/>
        <!-- Button 3: Bottom-Left Purple (Gear Icon) -->
        <rect x="148" y="214" width="94" height="94" rx="18" fill="#8B5CF6" stroke="#7C3AED" stroke-width="3"/>
        <circle cx="195" cy="261" r="18" stroke="#FFFFFF" stroke-width="9" fill="none"/>
        <circle cx="195" cy="261" r="7" fill="#8B5CF6"/>
        <g stroke="#FFFFFF" stroke-width="8" stroke-linecap="round">
          <line x1="195" y1="233" x2="195" y2="240"/>
          <line x1="195" y1="282" x2="195" y2="289"/>
          <line x1="167" y1="261" x2="174" y2="261"/>
          <line x1="216" y1="261" x2="223" y2="261"/>
          <line x1="175" y1="241" x2="180" y2="246"/>
          <line x1="210" y1="276" x2="215" y2="281"/>
          <line x1="215" y1="241" x2="210" y2="246"/>
          <line x1="180" y1="276" x2="175" y2="281"/>
        </g>
        <!-- Button 4: Bottom-Right Green (User Icon) -->
        <rect x="258" y="214" width="94" height="94" rx="18" fill="#22C55E" stroke="#16A34A" stroke-width="3"/>
        <circle cx="305" cy="247" r="14" fill="#FFFFFF"/>
        <path d="M281 286 C281 270, 292 265, 305 265 C318 265, 329 270, 329 286 Z" fill="#FFFFFF"/>
        <!-- Bottom UI Bar -->
        <rect x="148" y="330" width="204" height="22" rx="11" fill="#E2E8F0"/>
        <rect x="148" y="364" width="140" height="20" rx="10" fill="#E2E8F0"/>
        <rect x="205" y="432" width="90" height="7" rx="3.5" fill="#CBD5E1"/>
      </g>
    </svg>
    """,

    3: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Background Circle Blob -->
      <circle cx="245" cy="275" r="155" fill="#CBEAFB"/>
      <!-- Sound Waves on Left -->
      <path d="M98 228 C82 252, 82 292, 98 316" stroke="#2B88D8" stroke-width="11" stroke-linecap="round"/>
      <path d="M68 206 C44 244, 44 300, 68 338" stroke="#2B88D8" stroke-width="11" stroke-linecap="round"/>
      <path d="M126 248 C117 262, 117 282, 126 296" stroke="#2B88D8" stroke-width="10" stroke-linecap="round"/>
      <!-- Microphone Capsule -->
      <g filter="url(#dropShadow)">
        <rect x="198" y="168" width="84" height="142" rx="42" fill="#3B9AE8" stroke="#2574B8" stroke-width="5"/>
        <!-- Mic Specular Highlight -->
        <path d="M220 190 V255" stroke="#7CC4FA" stroke-width="9" stroke-linecap="round"/>
        <!-- Mic Cradle Arc -->
        <path d="M168 258 C168 308, 202 338, 240 338 C278 338, 312 308, 312 258" stroke="#2B88D8" stroke-width="14" stroke-linecap="round"/>
        <!-- Mic Stem & Base -->
        <line x1="240" y1="338" x2="240" y2="385" stroke="#2B88D8" stroke-width="14" stroke-linecap="round"/>
        <line x1="196" y1="385" x2="284" y2="385" stroke="#2B88D8" stroke-width="14" stroke-linecap="round"/>
      </g>
      <!-- Speech Bubble with 3 Dots (Top Right) -->
      <g filter="url(#dropShadow)">
        <path d="M295 105 H415 A34 34 0 0 1 449 139 V175 A34 34 0 0 1 415 209 H345 L312 236 L318 209 H295 A34 34 0 0 1 261 175 V139 A34 34 0 0 1 295 105 Z" fill="#2B88D8" stroke="#1E293B" stroke-width="5.5" stroke-linejoin="round"/>
        <circle cx="322" cy="157" r="11" fill="#FFFFFF"/>
        <circle cx="355" cy="157" r="11" fill="#FFFFFF"/>
        <circle cx="388" cy="157" r="11" fill="#FFFFFF"/>
      </g>
    </svg>
    """,

    4: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Background Circle Blob -->
      <circle cx="250" cy="278" r="168" fill="#CBEAFB"/>
      <!-- Stopwatch Top Plunger & Side Button -->
      <g filter="url(#dropShadow)">
        <!-- Top stem -->
        <rect x="234" y="64" width="32" height="38" rx="4" fill="#1D3557" stroke="#0F172A" stroke-width="4"/>
        <rect x="214" y="48" width="72" height="24" rx="6" fill="#1D3557" stroke="#0F172A" stroke-width="4"/>
        <!-- Angled right button -->
        <g transform="rotate(42 365 135)">
          <rect x="353" y="108" width="24" height="32" rx="4" fill="#1D3557" stroke="#0F172A" stroke-width="4"/>
          <rect x="345" y="96" width="40" height="16" rx="5" fill="#1D3557" stroke="#0F172A" stroke-width="4"/>
        </g>
        <!-- Main Outer Stopwatch Ring -->
        <circle cx="250" cy="272" r="168" fill="#1D3557" stroke="#0F172A" stroke-width="6"/>
        <!-- Inner White Clock Face -->
        <circle cx="250" cy="272" r="136" fill="#FFFFFF"/>
        <!-- Highlighted 2-Minute Speed Wedge (Purely visual + number 2, ZERO letters!) -->
        <path d="M250 272 L250 150 A122 122 0 0 1 356 211 Z" fill="#BAE6FD"/>
        <!-- Soft Inner Blue Ring -->
        <circle cx="250" cy="272" r="118" stroke="#93C5FD" stroke-width="14" fill="none"/>
        <!-- 12 Clock Tick Marks -->
        <g stroke="#1D3557" stroke-width="7" stroke-linecap="round">
          <line x1="250" y1="145" x2="250" y2="165"/>
          <line x1="250" y1="379" x2="250" y2="399"/>
          <line x1="123" y1="272" x2="143" y2="272"/>
          <line x1="357" y1="272" x2="377" y2="272"/>
          <line x1="313" y1="162" x2="303" y2="179"/>
          <line x1="360" y1="209" x2="343" y2="219"/>
          <line x1="360" y1="335" x2="343" y2="325"/>
          <line x1="313" y1="382" x2="303" y2="365"/>
          <line x1="187" y1="382" x2="197" y2="365"/>
          <line x1="140" y1="335" x2="157" y2="325"/>
          <line x1="140" y1="209" x2="157" y2="219"/>
          <line x1="187" y1="162" x2="197" y2="179"/>
        </g>
        <!-- Big Numeral "2" (Only number, zero letters!) -->
        <text x="250" y="308" text-anchor="middle" font-family="'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif" font-weight="900" font-size="118" fill="#1D3557">2</text>
        <!-- Two visual minute dots underneath instead of the word "min" -->
        <circle cx="234" cy="342" r="9" fill="#0284C7"/>
        <circle cx="266" cy="342" r="9" fill="#0284C7"/>
      </g>
    </svg>
    """,

    5: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Background Blob -->
      <ellipse cx="245" cy="275" rx="195" ry="155" fill="#CBEAFB"/>
      <!-- High-Contrast Clear Reading Card (ZERO letters - pure visual typography bars) -->
      <g filter="url(#dropShadow)">
        <rect x="48" y="105" width="380" height="275" rx="28" fill="#FFFFFF" stroke="#1E293B" stroke-width="6"/>
        <!-- Visual High-Contrast Header Block & Reading Bars (no 'Aa' letters!) -->
        <rect x="88" y="148" width="95" height="58" rx="14" fill="#1D3557"/>
        <rect x="104" y="164" width="63" height="10" rx="5" fill="#38BDF8"/>
        <rect x="104" y="182" width="42" height="10" rx="5" fill="#FFFFFF"/>
        <!-- Top Right Bars -->
        <rect x="210" y="152" width="175" height="18" rx="9" fill="#BDDDF4"/>
        <rect x="210" y="184" width="135" height="18" rx="9" fill="#BDDDF4"/>
        <!-- Full Width Clear Reading Lines -->
        <rect x="88" y="236" width="295" height="20" rx="10" fill="#CEE5F6"/>
        <rect x="88" y="274" width="245" height="20" rx="10" fill="#CEE5F6"/>
        <rect x="88" y="312" width="185" height="20" rx="10" fill="#CEE5F6"/>
      </g>
      <!-- Orange Eye Visibility Badge (Bottom Right) -->
      <g filter="url(#dropShadow)">
        <circle cx="388" cy="355" r="68" fill="#F5A623" stroke="#1E293B" stroke-width="6"/>
        <!-- Eye Outer Almond Shape -->
        <path d="M336 355 C352 325, 424 325, 440 355 C424 385, 352 385, 336 355 Z" fill="#FFFFFF" stroke="#1E293B" stroke-width="5" stroke-linejoin="round"/>
        <!-- Iris & Pupil -->
        <circle cx="388" cy="355" r="20" fill="#2B5B84" stroke="#1E293B" stroke-width="4"/>
        <circle cx="388" cy="355" r="9" fill="#0F172A"/>
        <!-- Eye Specular Glint -->
        <circle cx="395" cy="348" r="4.5" fill="#FFFFFF"/>
      </g>
    </svg>
    """,

    6: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Warm Peach Blob -->
      <circle cx="240" cy="268" r="172" fill="#FAD8CC"/>
      <!-- Encrypted Security Shield -->
      <g filter="url(#dropShadow)">
        <!-- Outer Shield Base -->
        <path d="M235 62 L395 128 V245 C395 348, 315 415, 235 446 C155 415, 75 348, 75 245 V128 L235 62 Z" fill="#4BA3E3" stroke="#1E293B" stroke-width="6" stroke-linejoin="round"/>
        <!-- Inner Shield Two-Tone Split -->
        <path d="M235 88 L368 143 V242 C368 328, 302 385, 235 412 C168 385, 102 328, 102 242 V143 L235 88 Z" fill="#2979FF" stroke="#1E293B" stroke-width="4" stroke-linejoin="round"/>
        <path d="M235 88 L368 143 V242 C368 328, 302 385, 235 412 V88 Z" fill="#1D63DC"/>
        <!-- White Padlock in Center -->
        <path d="M198 225 V190 C198 168, 214 152, 235 152 C256 152, 272 168, 272 190 V225" stroke="#FFFFFF" stroke-width="18" stroke-linecap="round" fill="none"/>
        <rect x="175" y="220" width="120" height="102" rx="20" fill="#FFFFFF" stroke="#1E293B" stroke-width="5"/>
        <!-- Keyhole -->
        <circle cx="235" cy="260" r="12" fill="#1D63DC"/>
        <path d="M229 266 L226 294 H244 L241 266 Z" fill="#1D63DC"/>
      </g>
      <!-- Green Checkmark Badge -->
      <g filter="url(#dropShadow)">
        <circle cx="378" cy="362" r="56" fill="#32B67A" stroke="#1E293B" stroke-width="6"/>
        <path d="M352 362 L370 380 L405 344" stroke="#FFFFFF" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </svg>
    """,

    7: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Warm Blob -->
      <circle cx="245" cy="272" r="168" fill="#FAD8CC"/>
      <!-- Vibration / Ringing Lines -->
      <g stroke="#E04F5F" stroke-width="10" stroke-linecap="round">
        <path d="M88 235 C70 268, 72 310, 95 340"/>
        <path d="M62 218 C38 262, 42 320, 72 358"/>
        <path d="M355 112 C388 128, 412 162, 415 200"/>
        <path d="M372 86 C415 106, 444 150, 446 198"/>
      </g>
      <!-- Tilted Red Alarm Bell -->
      <g transform="rotate(-10 235 255)" filter="url(#dropShadow)">
        <!-- Bell Top Loop -->
        <circle cx="235" cy="108" r="18" fill="#E04F5F" stroke="#1E293B" stroke-width="5.5"/>
        <!-- Bell Dome & Flared Lip -->
        <path d="M235 122 C172 122, 138 170, 138 242 C138 282, 118 308, 108 320 C102 328, 108 340, 122 340 H348 C362 340, 368 328, 362 320 C352 308, 332 282, 332 242 C332 170, 298 122, 235 122 Z" fill="#EA5262" stroke="#1E293B" stroke-width="6" stroke-linejoin="round"/>
        <!-- Bell Shading & Bottom Rim -->
        <ellipse cx="235" cy="340" rx="118" ry="16" fill="#C83747" stroke="#1E293B" stroke-width="5.5"/>
        <!-- Specular Left Highlight -->
        <path d="M168 185 C168 158, 188 145, 205 142" stroke="#F89AA4" stroke-width="12" stroke-linecap="round"/>
        <!-- Bell Clapper -->
        <circle cx="235" cy="368" r="24" fill="#D63E4E" stroke="#1E293B" stroke-width="5.5"/>
      </g>
      <!-- Blue Clock Badge (Bottom Right) -->
      <g filter="url(#dropShadow)">
        <circle cx="372" cy="356" r="66" fill="#4A90E2" stroke="#1E293B" stroke-width="6"/>
        <circle cx="372" cy="356" r="46" fill="#FFFFFF"/>
        <polyline points="372,324 372,356 392,372" stroke="#243447" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </g>
    </svg>
    """,

    8: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Warm Blob -->
      <circle cx="250" cy="295" r="165" fill="#FDE2C4"/>
      <!-- AI Brain / Circuit Cloud Bubble Above Robot -->
      <g filter="url(#dropShadow)">
        <path d="M215 148 C185 148, 168 126, 175 100 C165 76, 188 52, 215 58 C232 38, 272 38, 290 56 C318 46, 348 68, 342 96 C358 116, 342 146, 315 146 L298 172 L278 148 Z" fill="#54B6F8" stroke="#1E293B" stroke-width="5.5" stroke-linejoin="round"/>
        <!-- Circuit Lines & Nodes on Left of Brain -->
        <circle cx="210" cy="95" r="5" fill="#FFFFFF"/>
        <circle cx="245" cy="70" r="5" fill="#FFFFFF"/>
        <circle cx="232" cy="122" r="5" fill="#FFFFFF"/>
        <polyline points="210,95 210,78 245,78 245,122 232,122" stroke="#FFFFFF" stroke-width="3.5" fill="none"/>
        <!-- AI Gear on Right of Brain -->
        <circle cx="292" cy="98" r="16" fill="#1D63DC"/>
        <circle cx="292" cy="98" r="7" fill="#7CC4FA"/>
        <g stroke="#1D63DC" stroke-width="7" stroke-linecap="round">
          <line x1="292" y1="74" x2="292" y2="80"/>
          <line x1="292" y1="116" x2="292" y2="122"/>
          <line x1="268" y1="98" x2="274" y2="98"/>
          <line x1="310" y1="98" x2="316" y2="98"/>
          <line x1="275" y1="81" x2="280" y2="86"/>
          <line x1="304" y1="110" x2="309" y2="115"/>
          <line x1="309" y1="81" x2="304" y2="86"/>
          <line x1="280" y1="110" x2="275" y2="115"/>
        </g>
      </g>
      <!-- Cute AI Robot Head & Shoulders -->
      <g filter="url(#dropShadow)">
        <!-- Robot Torso / Shoulders -->
        <path d="M128 455 C135 408, 178 395, 238 395 C298 395, 341 408, 348 455 Z" fill="#E6F0FA" stroke="#1E293B" stroke-width="6"/>
        <!-- Neck -->
        <rect x="202" y="368" width="72" height="32" rx="10" fill="#1E293B"/>
        <!-- Tilted Robot Head -->
        <g transform="rotate(4 245 285)">
          <!-- Left & Right Ear Pods -->
          <ellipse cx="102" cy="292" rx="22" ry="44" fill="#D0E2F4" stroke="#1E293B" stroke-width="5.5"/>
          <ellipse cx="388" cy="292" rx="24" ry="46" fill="#3B9AE8" stroke="#1E293B" stroke-width="5.5"/>
          <!-- Outer White/Light-Blue Helmet -->
          <rect x="112" y="192" width="266" height="186" rx="64" fill="#F1F6FC" stroke="#1E293B" stroke-width="6"/>
          <!-- Inner Shading of Helmet -->
          <path d="M135 348 C175 372, 315 372, 355 348" stroke="#C5DCF2" stroke-width="16" stroke-linecap="round"/>
          <!-- Dark Visor Screen -->
          <rect x="138" y="218" width="214" height="134" rx="44" fill="#1E293B"/>
          <!-- Glowing Cyan Eyes -->
          <ellipse cx="192" cy="278" rx="18" ry="24" fill="#4CE0F5"/>
          <ellipse cx="298" cy="278" rx="18" ry="24" fill="#4CE0F5"/>
          <!-- Cute Cyan Smile -->
          <path d="M222 308 Q245 324 268 308" stroke="#4CE0F5" stroke-width="8" stroke-linecap="round" fill="none"/>
          <!-- Glossy Forehead Highlight -->
          <path d="M158 206 H202" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
        </g>
      </g>
    </svg>
    """,

    9: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Warm Blob -->
      <circle cx="245" cy="265" r="175" fill="#FDE2C4"/>
      <!-- Main Dark-Slate Privacy Circle -->
      <g filter="url(#dropShadow)">
        <circle cx="242" cy="258" r="168" fill="#52667A" stroke="#1E293B" stroke-width="6"/>
        <clipPath id="privacyClip9">
          <circle cx="242" cy="258" r="164"/>
        </clipPath>
        <g clip-path="url(#privacyClip9)">
          <!-- Secondary Background Silhouette (Right) -->
          <circle cx="322" cy="222" r="32" fill="#1D3557"/>
          <path d="M262 325 C262 282, 290 268, 322 268 C354 268, 382 282, 382 325 Z" fill="#1D3557"/>
          <!-- Foreground Main User Avatar (White Ring + Dark Center) -->
          <circle cx="212" cy="188" r="56" fill="#FFFFFF" stroke="#1E293B" stroke-width="5"/>
          <circle cx="212" cy="188" r="30" fill="#243447"/>
          <path d="M122 348 C122 276, 162 252, 212 252 C262 252, 302 276, 302 348 Z" fill="#FFFFFF" stroke="#1E293B" stroke-width="5"/>
          <path d="M150 348 C150 296, 178 278, 212 278 C246 278, 274 296, 274 348 Z" fill="#243447"/>
          <!-- Bottom darker wave inside circle -->
          <path d="M70 345 Q242 325 414 345 V430 H70 Z" fill="#3E5062" opacity="0.65"/>
        </g>
      </g>
      <!-- Green Padlock Badge (Bottom Right) -->
      <g filter="url(#dropShadow)">
        <circle cx="368" cy="364" r="58" fill="#2FA872" stroke="#1E293B" stroke-width="6"/>
        <path d="M350 354 V338 C350 326, 358 318, 368 318 C378 318, 386 326, 386 338 V354" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" fill="none"/>
        <rect x="340" y="350" width="56" height="44" rx="10" fill="#FFFFFF"/>
        <circle cx="368" cy="368" r="5.5" fill="#2FA872"/>
        <rect x="365.5" y="370" width="5" height="12" rx="2" fill="#2FA872"/>
      </g>
    </svg>
    """,

    10: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Warm Blob -->
      <circle cx="242" cy="278" r="168" fill="#FDE2C4"/>
      <!-- Prescription Pill Bottle -->
      <g filter="url(#dropShadow)">
        <!-- Bottle Neck -->
        <rect x="168" y="138" width="114" height="32" fill="#56A8F5" stroke="#1E293B" stroke-width="5.5"/>
        <!-- Orange Ribbed Cap -->
        <rect x="148" y="88" width="154" height="54" rx="14" fill="#E87A24" stroke="#1E293B" stroke-width="5.5"/>
        <!-- Cap Ribs -->
        <g stroke="#C65D10" stroke-width="5" stroke-linecap="round">
          <line x1="172" y1="98" x2="172" y2="132"/>
          <line x1="194" y1="98" x2="194" y2="132"/>
          <line x1="216" y1="98" x2="216" y2="132"/>
          <line x1="238" y1="98" x2="238" y2="132"/>
          <line x1="260" y1="98" x2="260" y2="132"/>
          <line x1="282" y1="98" x2="282" y2="132"/>
        </g>
        <!-- Blue Bottle Body -->
        <path d="M158 166 H292 L318 205 V415 A26 26 0 0 1 292 441 H158 A26 26 0 0 1 132 415 V205 L158 166 Z" fill="#3B9AE8" stroke="#1E293B" stroke-width="6" stroke-linejoin="round"/>
        <!-- Bottle Right Shading -->
        <path d="M275 170 L312 207 V415 A20 20 0 0 1 292 435 H275 Z" fill="#2574B8" opacity="0.5"/>
        <!-- White Label with Medical Cross -->
        <rect x="158" y="232" width="134" height="148" rx="18" fill="#FFFFFF" stroke="#1E293B" stroke-width="5"/>
        <!-- Orange Medical Cross -->
        <path d="M210 264 H240 V290 H266 V320 H240 V346 H210 V320 H184 V290 H210 Z" fill="#E87A24" stroke="#1E293B" stroke-width="4.5" stroke-linejoin="round"/>
      </g>
      <!-- Red Alert Bell Badge (Top Right) -->
      <g filter="url(#dropShadow)">
        <circle cx="368" cy="176" r="68" fill="#EA5262" stroke="#1E293B" stroke-width="5.5"/>
        <!-- White Bell inside Badge -->
        <circle cx="368" cy="132" r="7" fill="#FFFFFF"/>
        <path d="M368 138 C346 138, 336 154, 336 176 V192 L326 202 H410 L400 192 V176 C400 154, 390 138, 368 138 Z" fill="#FFFFFF"/>
        <circle cx="368" cy="212" r="10" fill="#FFFFFF"/>
      </g>
    </svg>
    """,

    11: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Blue Care Blob -->
      <circle cx="250" cy="285" r="168" fill="#CBEAFB"/>
      <!-- Floating Red Heart Above Care Circle -->
      <g filter="url(#dropShadow)">
        <path d="M250 208 C250 208, 178 160, 178 116 C178 88, 202 70, 226 70 C240 70, 250 80, 250 92 C250 80, 260 70, 274 70 C298 70, 322 88, 322 116 C322 160, 250 208, 250 208 Z" fill="#EA4C62" stroke="#1E293B" stroke-width="5.5" stroke-linejoin="round"/>
        <path d="M196 108 C196 95, 208 86, 220 86" stroke="#F89AA4" stroke-width="7" stroke-linecap="round"/>
      </g>
      <!-- Three Family / Care Circle Silhouettes -->
      <g filter="url(#dropShadow)">
        <!-- Left Person -->
        <circle cx="136" cy="262" r="44" fill="#1D4E78" stroke="#FFFFFF" stroke-width="4"/>
        <path d="M52 425 C52 348, 88 320, 136 320 C184 320, 220 348, 220 425 Z" fill="#1D4E78" stroke="#FFFFFF" stroke-width="4"/>
        <!-- Right Person -->
        <circle cx="364" cy="268" r="42" fill="#163B5C" stroke="#FFFFFF" stroke-width="4"/>
        <path d="M284 425 C284 352, 318 324, 364 324 C410 324, 444 352, 444 425 Z" fill="#163B5C" stroke="#FFFFFF" stroke-width="4"/>
        <!-- Center Child / Person in Front -->
        <circle cx="250" cy="306" r="38" fill="#25639A" stroke="#FFFFFF" stroke-width="5"/>
        <path d="M174 425 C174 366, 206 348, 250 348 C294 348, 326 366, 326 425 Z" fill="#25639A" stroke="#FFFFFF" stroke-width="5"/>
      </g>
    </svg>
    """,

    12: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Rose Blob -->
      <circle cx="248" cy="285" r="168" fill="#FAD8E2"/>
      <!-- Orange Alert Rays (Top Left) -->
      <g stroke="#F59E0B" stroke-width="11" stroke-linecap="round">
        <line x1="92" y1="88" x2="126" y2="112"/>
        <line x1="68" y1="132" x2="108" y2="144"/>
        <line x1="78" y1="182" x2="114" y2="176"/>
      </g>
      <!-- Tilted Smartphone -->
      <g transform="rotate(6 225 295)" filter="url(#dropShadow)">
        <rect x="110" y="95" width="230" height="370" rx="34" fill="#243447" stroke="#1E293B" stroke-width="6"/>
        <rect x="126" y="116" width="198" height="328" rx="20" fill="#CBE4F9" stroke="#1E293B" stroke-width="4"/>
        <!-- UI Bars on Phone Screen -->
        <rect x="152" y="346" width="135" height="16" rx="8" fill="#69A6DC"/>
        <rect x="152" y="374" width="115" height="16" rx="8" fill="#69A6DC"/>
        <rect x="152" y="402" width="145" height="16" rx="8" fill="#69A6DC"/>
      </g>
      <!-- Pop-out Alert Speech Bubble with Exclamation Mark -->
      <g transform="rotate(4 285 245)" filter="url(#dropShadow)">
        <path d="M188 148 H382 A32 32 0 0 1 414 180 V284 A32 32 0 0 1 382 316 H252 L205 352 L214 316 H188 A32 32 0 0 1 156 284 V180 A32 32 0 0 1 188 148 Z" fill="#FFFFFF" stroke="#1E293B" stroke-width="5.5" stroke-linejoin="round"/>
        <!-- Red Circle with White '!' -->
        <circle cx="285" cy="232" r="58" fill="#EA5262"/>
        <rect x="277" y="194" width="16" height="44" rx="8" fill="#FFFFFF"/>
        <circle cx="285" cy="258" r="9" fill="#FFFFFF"/>
      </g>
    </svg>
    """,

    13: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Mint Blob -->
      <circle cx="248" cy="278" r="168" fill="#C9F0E4"/>
      <!-- Tilted Progress Report Card -->
      <g transform="rotate(3 245 268)" filter="url(#dropShadow)">
        <rect x="88" y="75" width="310" height="380" rx="28" fill="#FFFFFF" stroke="#1E293B" stroke-width="5.5"/>
        <!-- Top Header Bars -->
        <rect x="128" y="116" width="175" height="18" rx="9" fill="#94A3B8"/>
        <rect x="128" y="146" width="120" height="16" rx="8" fill="#CBD5E1"/>
        <!-- 4 Rising Bar Chart Columns -->
        <!-- Bar 1 (Purple) -->
        <rect x="132" y="274" width="38" height="72" rx="8" fill="#7C3AED"/>
        <rect x="132" y="298" width="38" height="48" rx="6" fill="#A855F7"/>
        <!-- Bar 2 (Magenta-Violet) -->
        <rect x="188" y="236" width="38" height="110" rx="8" fill="#6D28D9"/>
        <rect x="188" y="278" width="38" height="68" rx="6" fill="#C026D3"/>
        <!-- Bar 3 (Blue) -->
        <rect x="244" y="198" width="38" height="148" rx="8" fill="#2563EB"/>
        <rect x="244" y="246" width="38" height="100" rx="6" fill="#3B82F6"/>
        <!-- Bar 4 (Emerald Green) -->
        <rect x="300" y="162" width="38" height="184" rx="8" fill="#10B981"/>
        <!-- Bottom Summary Lines -->
        <rect x="126" y="366" width="225" height="16" rx="8" fill="#94A3B8"/>
        <rect x="126" y="394" width="175" height="16" rx="8" fill="#CBD5E1"/>
      </g>
      <!-- Teal-Green Checkmark Badge (Top Right) -->
      <g filter="url(#dropShadow)">
        <circle cx="388" cy="118" r="48" fill="#26A688" stroke="#FFFFFF" stroke-width="5"/>
        <path d="M366 118 L382 134 L412 102" stroke="#FFFFFF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </svg>
    """,

    14: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Warm Cream/Gold Blob -->
      <circle cx="248" cy="278" r="172" fill="#FDE5C0"/>
      <!-- Earth Globe -->
      <g filter="url(#dropShadow)">
        <circle cx="245" cy="276" r="162" fill="#1E88E5" stroke="#1E293B" stroke-width="5.5"/>
        <clipPath id="globeClip14">
          <circle cx="245" cy="276" r="159"/>
        </clipPath>
        <g clip-path="url(#globeClip14)">
          <!-- Green Continents -->
          <path d="M82 175 C125 162, 165 188, 175 225 C185 262, 152 295, 168 335 C182 372, 155 418, 115 425 L65 360 Z" fill="#43A047"/>
          <path d="M258 122 C298 118, 355 142, 378 185 C400 228, 372 268, 388 312 C402 355, 368 415, 318 408 C282 402, 275 348, 295 312 C315 276, 245 245, 255 195 Z" fill="#2E7D32"/>
          <path d="M188 118 C215 112, 242 132, 232 158 C222 184, 185 172, 188 118 Z" fill="#66BB6A"/>
          <!-- Dashed Connectivity Bridges -->
          <path d="M142 325 Q248 275 352 195" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="12 10" stroke-linecap="round" fill="none"/>
          <path d="M142 325 Q215 215 198 158" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="10 9" stroke-linecap="round" fill="none"/>
          <path d="M352 195 Q368 285 335 355" stroke="#FFFFFF" stroke-width="5" stroke-dasharray="10 9" stroke-linecap="round" fill="none"/>
        </g>
      </g>
      <!-- Location Pin 1 (Bottom Left) -->
      <g filter="url(#dropShadow)">
        <path d="M142 358 C142 358, 96 304, 96 268 C96 242, 116 222, 142 222 C168 222, 188 242, 188 268 C188 304, 142 358, 142 358 Z" fill="#EC407A" stroke="#FFFFFF" stroke-width="5"/>
        <path d="M142 286 C142 286, 120 270, 120 256 C120 247, 128 241, 135 241 C139 241, 142 244, 142 248 C142 244, 145 241, 149 241 C156 241, 164 247, 164 256 C164 270, 142 286, 142 286 Z" fill="#FFFFFF"/>
      </g>
      <!-- Location Pin 2 (Top Right) -->
      <g filter="url(#dropShadow)">
        <path d="M355 218 C355 218, 312 168, 312 134 C312 110, 331 92, 355 92 C379 92, 398 110, 398 134 C398 168, 355 218, 355 218 Z" fill="#EC407A" stroke="#FFFFFF" stroke-width="5"/>
        <path d="M355 152 C355 152, 335 137, 335 124 C335 116, 342 110, 349 110 C352 110, 355 113, 355 117 C355 113, 358 110, 361 110 C368 110, 375 116, 375 124 C375 137, 355 152, 355 152 Z" fill="#FFFFFF"/>
      </g>
      <!-- Small Heart Node 3 (Top Center-Left) -->
      <path d="M202 178 C202 178, 174 158, 174 140 C174 128, 184 120, 194 120 C199 120, 202 124, 202 128 C202 124, 205 120, 210 120 C220 120, 230 128, 230 140 C230 158, 202 178, 202 178 Z" fill="#EC407A" stroke="#1E293B" stroke-width="4"/>
      <!-- Small Heart Node 4 (Bottom Right) -->
      <path d="M332 378 C332 378, 304 358, 304 340 C304 328, 314 320, 324 320 C329 320, 332 324, 332 328 C332 324, 335 320, 340 320 C350 320, 360 328, 360 340 C360 358, 332 378, 332 378 Z" fill="#EC407A" stroke="#1E293B" stroke-width="4"/>
    </svg>
    """,

    15: """
    <svg viewBox="0 0 500 500" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Soft Lavender/Pink Glow Blob -->
      <circle cx="250" cy="275" r="172" fill="#F6D5EB"/>
      <!-- Golden Sparkles -->
      <path d="M412 95 L422 122 L449 132 L422 142 L412 169 L402 142 L375 132 L402 122 Z" fill="#FBBF24"/>
      <path d="M88 338 L96 358 L116 366 L96 374 L88 394 L80 374 L60 366 L80 358 Z" fill="#FBBF24"/>
      <path d="M122 392 L127 406 L141 411 L127 416 L122 430 L117 416 L103 411 L117 406 Z" fill="#F59E0B"/>
      <!-- Large Vibrant Heart with ECG Pulse Line -->
      <g filter="url(#dropShadow)">
        <path d="M250 422 C250 422, 78 312, 78 192 C78 130, 126 86, 182 86 C216 86, 240 106, 250 128 C260 106, 284 86, 318 86 C374 86, 422 130, 422 192 C422 312, 250 422, 250 422 Z" fill="#EC4067" stroke="#881337" stroke-width="5.5" stroke-linejoin="round"/>
        <!-- Heart Left Glossy Highlight -->
        <path d="M112 186 C112 145, 142 118, 178 118" stroke="#F988A2" stroke-width="14" stroke-linecap="round"/>
        <!-- White ECG Heartbeat Line -->
        <polyline points="105,256 185,256 212,188 242,324 272,226 292,256 395,256" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </g>
    </svg>
    """,
}

# Section visual icons (NO letters/words)
SECTION_ICONS = {
    1: """
    <!-- Section 1 Icon: Hand Touch / Tap Icon (Easy to Use) -->
    <svg viewBox="0 0 80 80" width="54" height="54" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="40" cy="24" r="14" stroke="#FFFFFF" stroke-width="3.5" opacity="0.7"/>
      <circle cx="40" cy="24" r="8" stroke="#FFFFFF" stroke-width="3.5"/>
      <path d="M35 24 V48 L27 42 C24 40, 20 42, 22 46 L33 62 C36 66, 40 68, 46 68 H54 C60 68, 64 63, 64 56 V42 C64 38, 59 38, 59 41 V39 C59 35, 54 35, 54 39 V37 C54 33, 49 33, 49 37 V40 H45 V24 C45 20, 35 20, 35 24 Z" fill="#FFFFFF"/>
    </svg>
    """,
    2: """
    <!-- Section 2 Icon: Padlock Icon (Smart & Secure) -->
    <svg viewBox="0 0 80 80" width="54" height="54" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M27 36 V26 C27 18, 33 12, 40 12 C47 12, 53 18, 53 26 V36" stroke="#FFFFFF" stroke-width="6.5" stroke-linecap="round"/>
      <rect x="20" y="34" width="40" height="34" rx="8" fill="#FFFFFF"/>
      <circle cx="40" cy="48" r="4.5" fill="#EA580C"/>
      <path d="M38 50 L36 60 H44 L42 50 Z" fill="#EA580C"/>
    </svg>
    """,
    3: """
    <!-- Section 3 Icon: Care Circle / Connected Nodes Icon (Always Connected) -->
    <svg viewBox="0 0 80 80" width="54" height="54" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line x1="24" y1="54" x2="40" y2="24" stroke="#FFFFFF" stroke-width="5"/>
      <line x1="56" y1="54" x2="40" y2="24" stroke="#FFFFFF" stroke-width="5"/>
      <line x1="24" y1="54" x2="56" y2="54" stroke="#FFFFFF" stroke-width="5"/>
      <circle cx="40" cy="24" r="10" fill="#FFFFFF"/>
      <circle cx="24" cy="54" r="10" fill="#FFFFFF"/>
      <circle cx="56" cy="54" r="10" fill="#FFFFFF"/>
    </svg>
    """,
}

SECTION_THEMES = {
    1: {
        "bg_grad": "radial-gradient(circle at 18% 22%, #0F3D5E 0%, #0A2239 52%, #061524 100%)",
        "orb1": "#0EA5E9",
        "orb2": "#14B8A6",
        "pill_bg": "linear-gradient(135deg, #128277 0%, #20A495 100%)",
        "ring_color": "#38BDF8",
        "card_border": "rgba(56, 189, 248, 0.35)",
    },
    2: {
        "bg_grad": "radial-gradient(circle at 18% 22%, #4A1D1F 0%, #2B1216 52%, #180A0D 100%)",
        "orb1": "#F97316",
        "orb2": "#F43F5E",
        "pill_bg": "linear-gradient(135deg, #EA580C 0%, #F59E0B 100%)",
        "ring_color": "#FB923C",
        "card_border": "rgba(251, 146, 60, 0.35)",
    },
    3: {
        "bg_grad": "radial-gradient(circle at 18% 22%, #2E1A47 0%, #1A102B 52%, #0F091C 100%)",
        "orb1": "#8B5CF6",
        "orb2": "#EC4899",
        "pill_bg": "linear-gradient(135deg, #5B21B6 0%, #7C3AED 100%)",
        "ring_color": "#A78BFA",
        "card_border": "rgba(167, 139, 250, 0.35)",
    },
}


def build_slide_html_fragment(item: dict) -> str:
    num = item["num"]
    sec = item["section"]
    theme = SECTION_THEMES[sec]
    svg_art = SVG_ILLUSTRATIONS[num]
    sec_icon = SECTION_ICONS[sec]

    # Build 15-dot progress bar at bottom (purely visual + numbers 1..15)
    dots_html = []
    for i in range(1, 16):
        dot_sec = 1 if i <= 5 else (2 if i <= 10 else 3)
        dot_col = "#38BDF8" if dot_sec == 1 else ("#FB923C" if dot_sec == 2 else "#A78BFA")
        if i == num:
            dots_html.append(
                f'<div class="prog-dot active" data-slide="{i-1}" style="background:{item["badge_color"]}; border-color:#FFFFFF; box-shadow: 0 0 22px {dot_col};">{i}</div>'
            )
        elif i < num:
            dots_html.append(
                f'<div class="prog-dot done" data-slide="{i-1}" style="background:rgba(255,255,255,0.18); border-color:{dot_col}; color:#E2E8F0;">{i}</div>'
            )
        else:
            dots_html.append(
                f'<div class="prog-dot" data-slide="{i-1}">{i}</div>'
            )
        if i in (5, 10):
            dots_html.append('<div class="prog-divider"></div>')

    # Build 5-dot mini group indicator on left panel
    group_start = (sec - 1) * 5 + 1
    mini_dots = []
    for g in range(group_start, group_start + 5):
        if g == num:
            mini_dots.append(f'<span class="mini-dot active" style="background:{theme["ring_color"]}; box-shadow:0 0 12px {theme["ring_color"]};"></span>')
        elif g < num:
            mini_dots.append(f'<span class="mini-dot past" style="background:{theme["ring_color"]}; opacity:0.55;"></span>')
        else:
            mini_dots.append('<span class="mini-dot"></span>')

    return f"""
    <section class="slide" id="slide-{num}" data-num="{num}" style="background: {theme['bg_grad']};">
      <!-- Ambient glowing orbs -->
      <div class="orb orb-1" style="background: {theme['orb1']};"></div>
      <div class="orb orb-2" style="background: {theme['orb2']};"></div>
      <div class="orb orb-3" style="background: {item['accent_glow']};"></div>

      <!-- Decorative botanical corner leaves (like the infographic header/footer) -->
      <svg class="corner-leaves top-left-leaves" viewBox="0 0 260 260" fill="none">
        <path d="M-20 180 C40 160, 95 110, 110 30 C50 40, 5 90, -20 180 Z" fill="#10B981" opacity="0.16"/>
        <path d="M-10 240 C70 210, 145 150, 175 55 C95 70, 35 135, -10 240 Z" fill="#14B8A6" opacity="0.13"/>
        <path d="M40 -20 C65 55, 120 105, 205 120 C185 55, 125 5, 40 -20 Z" fill="#38BDF8" opacity="0.12"/>
      </svg>
      <svg class="corner-leaves bottom-right-leaves" viewBox="0 0 260 260" fill="none">
        <path d="M280 80 C220 100, 165 150, 150 230 C210 220, 255 170, 280 80 Z" fill="#10B981" opacity="0.16"/>
        <path d="M270 20 C190 50, 115 110, 85 205 C165 190, 225 125, 270 20 Z" fill="#14B8A6" opacity="0.13"/>
      </svg>

      <!-- Main 2-Column Stage -->
      <div class="slide-content">
        <!-- Left Hero Number Pedestal (Zero letters!) -->
        <div class="left-pedestal" style="border-color: {theme['card_border']};">
          <!-- Top Brand Pill Icon + Section Visual Badge -->
          <div class="top-badges-row">
            <!-- MedReminder Capsule Pill Icon -->
            <div class="capsule-badge" title="MedReminder AI">
              <svg viewBox="0 0 64 64" width="42" height="42" fill="none">
                <g transform="rotate(-38 32 32)">
                  <rect x="18" y="8" width="28" height="48" rx="14" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="3"/>
                  <path d="M18 32 H46 V42 A14 14 0 0 1 18 42 Z" fill="#38BDF8"/>
                  <line x1="18" y1="32" x2="46" y2="32" stroke="#0284C7" stroke-width="3"/>
                </g>
              </svg>
            </div>
            <!-- Category Visual Icon Pill -->
            <div class="section-icon-pill" style="background: {theme['pill_bg']};">
              {sec_icon}
            </div>
          </div>

          <!-- Giant Glowing Number Badge -->
          <div class="number-halo-wrap">
            <div class="number-outer-ring" style="border-color: {theme['ring_color']}; box-shadow: 0 0 65px {item['accent_glow']}55;">
              <div class="number-circle" style="background: {item['badge_color']};">
                <span class="number-digits">{num}</span>
              </div>
            </div>
          </div>

          <!-- 5-dot Section Progress Indicator -->
          <div class="mini-dots-row">
            {''.join(mini_dots)}
          </div>
        </div>

        <!-- Right Visual Illustration Stage -->
        <div class="right-stage-wrap">
          <div class="illustration-card" style="background: {item['card_bg']}; border-color: {theme['card_border']}; box-shadow: 0 35px 90px rgba(0,0,0,0.45), 0 0 70px {item['accent_glow']}33;">
            <!-- Corner subtle number watermark -->
            <div class="card-corner-badge" style="background: {item['badge_color']};">{num}</div>
            <!-- Vector Illustration -->
            <div class="artwork-container">
              {svg_art}
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom 15-Number Visual Timeline Dock -->
      <div class="bottom-timeline">
        {''.join(dots_html)}
      </div>

      <!-- Hidden Study Cheat-Sheet Overlay (OFF by default; toggled only with 'S' key in browser) -->
      <div class="study-note-overlay">
        <span class="study-num">#{num}</span>
        <span class="study-sentence">{escape(item['sentence'])}</span>
      </div>
    </section>
    """


def generate_html_file(html_path: str):
    slides_fragments = "\n".join(build_slide_html_fragment(item) for item in SLIDES_META)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080, initial-scale=1.0" />
<title>MedReminder AI — 15 Visual Slides</title>
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
  }}
  html, body {{
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    background: #061524;
    font-family: -apple-system, BlinkMacSystemFont, "Plus Jakarta Sans", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}

  /* Shared SVG drop shadow filter */
  .svg-defs {{
    position: absolute;
    width: 0;
    height: 0;
    overflow: hidden;
  }}

  .deck-viewport {{
    position: relative;
    width: 1920px;
    height: 1080px;
    overflow: hidden;
  }}

  .slide {{
    position: absolute;
    inset: 0;
    width: 1920px;
    height: 1080px;
    display: none;
    overflow: hidden;
  }}
  .slide.active {{
    display: block;
  }}

  /* Ambient glowing background orbs */
  .orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(110px);
    opacity: 0.28;
    pointer-events: none;
  }}
  .orb-1 {{
    width: 680px;
    height: 680px;
    top: -180px;
    left: -140px;
  }}
  .orb-2 {{
    width: 760px;
    height: 760px;
    bottom: -240px;
    right: -160px;
  }}
  .orb-3 {{
    width: 520px;
    height: 520px;
    top: 220px;
    left: 780px;
    opacity: 0.18;
  }}

  .corner-leaves {{
    position: absolute;
    width: 340px;
    height: 340px;
    pointer-events: none;
  }}
  .top-left-leaves {{
    top: 0;
    left: 0;
  }}
  .bottom-right-leaves {{
    bottom: 0;
    right: 0;
  }}

  /* Main 2-column content area */
  .slide-content {{
    position: relative;
    z-index: 5;
    width: 1720px;
    height: 820px;
    margin: 64px auto 0 auto;
    display: grid;
    grid-template-columns: 520px 1fr;
    gap: 68px;
    align-items: center;
  }}

  /* Left Glass Pedestal */
  .left-pedestal {{
    height: 740px;
    border-radius: 44px;
    background: rgba(255, 255, 255, 0.055);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 2px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 30px 70px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.25);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 46px 36px;
  }}

  .top-badges-row {{
    display: flex;
    align-items: center;
    gap: 20px;
  }}

  .capsule-badge {{
    width: 78px;
    height: 78px;
    border-radius: 24px;
    background: rgba(15, 23, 42, 0.65);
    border: 2px solid rgba(255, 255, 255, 0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.3);
  }}

  .section-icon-pill {{
    width: 118px;
    height: 78px;
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid rgba(255, 255, 255, 0.32);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.3);
  }}

  /* Giant Number Circle */
  .number-halo-wrap {{
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px 0;
  }}

  .number-outer-ring {{
    width: 340px;
    height: 340px;
    border-radius: 50%;
    border: 4px dashed rgba(255, 255, 255, 0.35);
    padding: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0) 70%);
  }}

  .number-circle {{
    width: 280px;
    height: 280px;
    border-radius: 50%;
    border: 8px solid #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 22px 50px rgba(0, 0, 0, 0.45), inset 0 8px 18px rgba(255, 255, 255, 0.35);
  }}

  .number-digits {{
    font-size: 148px;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1;
    letter-spacing: -4px;
    text-shadow: 0 8px 20px rgba(0, 0, 0, 0.28);
  }}

  .mini-dots-row {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .mini-dot {{
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.18);
    transition: all 0.25s ease;
  }}
  .mini-dot.active {{
    width: 48px;
    border-radius: 12px;
  }}

  /* Right Stage Card */
  .right-stage-wrap {{
    height: 740px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .illustration-card {{
    position: relative;
    width: 100%;
    height: 740px;
    border-radius: 48px;
    border: 6px solid rgba(255, 255, 255, 0.85);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}

  /* Subtle inner sheen */
  .illustration-card::before {{
    content: "";
    position: absolute;
    inset: 14px;
    border-radius: 36px;
    border: 3px dashed rgba(30, 41, 59, 0.10);
    pointer-events: none;
  }}

  .card-corner-badge {{
    position: absolute;
    top: 32px;
    left: 36px;
    width: 78px;
    height: 78px;
    border-radius: 50%;
    color: #FFFFFF;
    font-size: 38px;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 4px solid #FFFFFF;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
    z-index: 3;
  }}

  .artwork-container {{
    width: 650px;
    height: 650px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
  }}

  /* Bottom 15-Number Visual Timeline */
  .bottom-timeline {{
    position: absolute;
    bottom: 38px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 28px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(16px);
    border: 1.5px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
  }}

  .prog-dot {{
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.07);
    border: 2px solid rgba(255, 255, 255, 0.16);
    color: rgba(255, 255, 255, 0.45);
    font-size: 19px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .prog-dot.active {{
    width: 58px;
    height: 58px;
    color: #FFFFFF;
    font-size: 24px;
    transform: translateY(-4px);
  }}
  .prog-divider {{
    width: 2px;
    height: 28px;
    background: rgba(255, 255, 255, 0.18);
    margin: 0 6px;
  }}

  /* Study Note Overlay (Hidden unless user presses S in interactive mode) */
  .study-note-overlay {{
    display: none;
    position: absolute;
    top: 22px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 30;
    background: rgba(15, 23, 42, 0.92);
    border: 2px solid rgba(56, 189, 248, 0.5);
    color: #F8FAFC;
    padding: 14px 32px;
    border-radius: 999px;
    font-size: 26px;
    font-weight: 600;
    box-shadow: 0 18px 40px rgba(0,0,0,0.5);
    gap: 16px;
    align-items: center;
  }}
  body.show-study .study-note-overlay {{
    display: inline-flex;
  }}
  .study-num {{
    color: #38BDF8;
    font-weight: 900;
  }}
</style>
</head>
<body>
  <!-- Shared SVG Filter Definitions -->
  <svg class="svg-defs" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="dropShadow" x="-15%" y="-15%" width="135%" height="135%">
        <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.18"/>
      </filter>
    </defs>
  </svg>

  <div class="deck-viewport" id="deck">
    {slides_fragments}
  </div>

  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    let current = 0;

    function showSlide(index) {{
      if (index < 0) index = 0;
      if (index >= slides.length) index = slides.length - 1;
      current = index;
      slides.forEach((s, i) => s.classList.toggle('active', i === current));
      window.location.hash = '#' + (current + 1);
    }}

    // Check initial hash (#1 .. #15)
    function syncFromHash() {{
      const h = parseInt(window.location.hash.replace('#', ''), 10);
      if (!isNaN(h) && h >= 1 && h <= slides.length) {{
        showSlide(h - 1);
      }} else {{
        showSlide(0);
      }}
    }}
    window.addEventListener('hashchange', syncFromHash);
    syncFromHash();

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        e.preventDefault();
        showSlide(current + 1);
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        showSlide(current - 1);
      }} else if (e.key === 'Home') {{
        showSlide(0);
      }} else if (e.key === 'End') {{
        showSlide(slides.length - 1);
      }} else if (e.key === 's' || e.key === 'S') {{
        document.body.classList.toggle('show-study');
      }} else if (e.key === 'f' || e.key === 'F') {{
        if (!document.fullscreenElement) {{
          document.documentElement.requestFullscreen().catch(() => {{}});
        }} else {{
          document.exitFullscreen().catch(() => {{}});
        }}
      }}
    }});

    // Click on bottom timeline dots
    document.querySelectorAll('.prog-dot').forEach((dot) => {{
      dot.addEventListener('click', (e) => {{
        e.stopPropagation();
        const idx = parseInt(dot.getAttribute('data-slide'), 10);
        if (!isNaN(idx)) showSlide(idx);
      }});
    }});

    // Responsive scaling when opened in normal browser window
    function fitViewport() {{
      const deck = document.getElementById('deck');
      const scaleX = window.innerWidth / 1920;
      const scaleY = window.innerHeight / 1080;
      const scale = Math.min(scaleX, scaleY);
      if (Math.abs(scale - 1) > 0.01) {{
        deck.style.transformOrigin = 'top left';
        deck.style.transform = `scale(${{scale}})`;
        const leftPad = Math.max(0, (window.innerWidth - 1920 * scale) / 2);
        const topPad = Math.max(0, (window.innerHeight - 1080 * scale) / 2);
        deck.style.marginLeft = leftPad + 'px';
        deck.style.marginTop = topPad + 'px';
      }} else {{
        deck.style.transform = '';
        deck.style.marginLeft = '0';
        deck.style.marginTop = '0';
      }}
    }}
    window.addEventListener('resize', fitViewport);
    fitViewport();
  </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def render_slides_with_chrome(html_path: str) -> list[str]:
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    png_paths = []
    for i in range(1, 16):
        out_png = os.path.join(SCRATCH_DIR, f"slide_{i:02d}.png")
        url = f"file://{html_path}#{i}"
        cmd = [
            chrome_bin,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1920,1080",
            "--force-device-scale-factor=1",
            f"--screenshot={out_png}",
            url,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        png_paths.append(out_png)
    return png_paths


def build_pptx_from_pngs(png_paths: list[str], out_pptx: str):
    """
    Creates a valid 16:9 widescreen PowerPoint (.pptx) file with 15 slides
    (full-bleed 1920x1080 PNG on each slide, ZERO text on slides, and speaker notes
    attached to each slide for Presenter View).
    """
    # 16:9 widescreen in EMUs (13.333 in x 7.5 in)
    CX = 12192000
    CY = 6858000

    with zipfile.ZipFile(out_pptx, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. [Content_Types].xml
        slide_overrides = []
        for i in range(1, len(png_paths) + 1):
            slide_overrides.append(
                f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            )
            slide_overrides.append(
                f'  <Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
            )
        content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
{chr(10).join(slide_overrides)}
</Types>"""
        zf.writestr("[Content_Types].xml", content_types)

        # 2. _rels/.rels
        root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""
        zf.writestr("_rels/.rels", root_rels)

        # 3. ppt/_rels/presentation.xml.rels
        pres_rels_items = [
            '  <Relationship Id="rIdMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
            '  <Relationship Id="rIdNotesMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>',
            '  <Relationship Id="rIdTheme1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>',
        ]
        slide_id_Items = []
        for i in range(1, len(png_paths) + 1):
            pres_rels_items.append(
                f'  <Relationship Id="rIdSlide{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
            )
            slide_id_Items.append(f'    <p:sldId id="{255 + i}" r:id="rIdSlide{i}"/>')

        pres_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{chr(10).join(pres_rels_items)}
</Relationships>"""
        zf.writestr("ppt/_rels/presentation.xml.rels", pres_rels)

        # 4. ppt/presentation.xml
        presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rIdMaster1"/>
  </p:sldMasterIdLst>
  <p:notesMasterIdLst>
    <p:notesMasterId r:id="rIdNotesMaster1"/>
  </p:notesMasterIdLst>
  <p:sldIdLst>
{chr(10).join(slide_id_Items)}
  </p:sldIdLst>
  <p:sldSz cx="{CX}" cy="{CY}"/>
  <p:notesSz cx="{CY}" cy="{CX}"/>
</p:presentation>"""
        zf.writestr("ppt/presentation.xml", presentation_xml)

        # 5. Minimal SlideMaster, SlideLayout, NotesMaster, Theme
        slide_master_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rIdLayout1"/></p:sldLayoutIdLst>
</p:sldMaster>"""
        zf.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml)

        slide_master_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdLayout1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdTheme1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels)

        slide_layout_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml)

        slide_layout_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels)

        notes_master_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notesMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
               xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
               xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
</p:notesMaster>"""
        zf.writestr("ppt/notesMasters/notesMaster1.xml", notes_master_xml)

        notes_master_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdTheme1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""
        zf.writestr("ppt/notesMasters/_rels/notesMaster1.xml.rels", notes_master_rels)

        theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="MedReminderTheme">
  <a:themeElements>
    <a:clrScheme name="MedReminder">
      <a:dk1><a:srgbClr val="0F172A"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1E293B"/></a:dk2>
      <a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="0284C7"/></a:accent1>
      <a:accent2><a:srgbClr val="EA580C"/></a:accent2>
      <a:accent3><a:srgbClr val="7C3AED"/></a:accent3>
      <a:accent4><a:srgbClr val="10B981"/></a:accent4>
      <a:accent5><a:srgbClr val="F59E0B"/></a:accent5>
      <a:accent6><a:srgbClr val="EC4899"/></a:accent6>
      <a:hlink><a:srgbClr val="0284C7"/></a:hlink>
      <a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="MedReminderFonts">
      <a:majorFont><a:latin typeface="Helvetica Neue"/></a:majorFont>
      <a:minorFont><a:latin typeface="Helvetica Neue"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="MedReminderFmt">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>"""
        zf.writestr("ppt/theme/theme1.xml", theme_xml)

        # 6. Each Slide + Image + Speaker Notes
        for i, png_path in enumerate(png_paths, start=1):
            img_name = f"slide{i}.png"
            zf.write(png_path, f"ppt/media/{img_name}")

            slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
      <p:pic>
        <p:nvPicPr>
          <p:cNvPr id="2" name="SlideImage{i}"/>
          <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
          <p:nvPr/>
        </p:nvPicPr>
        <p:blipFill>
          <a:blip r:embed="rIdImg1"/>
          <a:stretch><a:fillRect/></a:stretch>
        </p:blipFill>
        <p:spPr>
          <a:xfrm>
            <a:off x="0" y="0"/>
            <a:ext cx="{CX}" cy="{CY}"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
      </p:pic>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""
            zf.writestr(f"ppt/slides/slide{i}.xml", slide_xml)

            slide_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdLayout1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdImg1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{img_name}"/>
  <Relationship Id="rIdNotes1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{i}.xml"/>
</Relationships>"""
            zf.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels)

            meta = SLIDES_META[i - 1]
            note_text = f"Slide #{i}: {meta['sentence']}  (Passive voice: {meta['verb_focus']})"
            notes_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
         xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
         xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr/>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Notes Placeholder"/><p:cNvSpPr/><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>
        <p:spPr/>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p><a:r><a:rPr lang="en-US" sz="1600" b="1"/><a:t>{escape(note_text)}</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:notes>"""
            zf.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notes_xml)

            notes_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdSlide1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{i}.xml"/>
  <Relationship Id="rIdNotesMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="../notesMasters/notesMaster1.xml"/>
</Relationships>"""
            zf.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", notes_rels)


def build_pdf_from_pngs(png_paths: list[str], out_pdf: str):
    images = [Image.open(p).convert("RGB") for p in png_paths]
    images[0].save(out_pdf, "PDF", resolution=150.0, save_all=True, append_images=images[1:])


def build_contact_sheet(png_paths: list[str], out_sheet: str):
    """Creates a 5x3 overview grid image of all 15 slides for quick visual inspection."""
    thumb_w, thumb_h = 480, 270
    pad = 20
    cols, rows = 5, 3
    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = rows * thumb_h + (rows + 1) * pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), (10, 18, 32))
    for idx, p in enumerate(png_paths):
        r = idx // cols
        c = idx % cols
        im = Image.open(p).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad + c * (thumb_w + pad)
        y = pad + r * (thumb_h + pad)
        sheet.paste(im, (x, y))
    sheet.save(out_sheet, quality=92)


def main():
    html_out = os.path.join(OUT_DIR_DEV, "MedReminderAI_Presentacion_Interactiva.html")
    pptx_out = os.path.join(OUT_DIR_DEV, "MedReminderAI_Presentacion_15_Numeros.pptx")
    pdf_out = os.path.join(OUT_DIR_DEV, "MedReminderAI_Presentacion_15_Numeros.pdf")
    sheet_out = os.path.join(ARTIFACT_DIR, "vista_previa_15_diapositivas.png")

    print("1. Generating interactive HTML5 presentation...")
    generate_html_file(html_out)

    print("2. Rendering 15 Full HD (1920x1080) slides via Headless Chrome...")
    png_paths = render_slides_with_chrome(html_out)

    print("3. Packaging 16:9 PowerPoint (.pptx) with speaker notes...")
    build_pptx_from_pngs(png_paths, pptx_out)

    print("4. Packaging 16:9 Full HD PDF presentation...")
    build_pdf_from_pngs(png_paths, pdf_out)

    print("5. Building overview contact sheet & copying previews...")
    build_contact_sheet(png_paths, sheet_out)
    for sample_idx in [1, 4, 5, 8, 10, 14, 15]:
        shutil.copy(
            png_paths[sample_idx - 1],
            os.path.join(ARTIFACT_DIR, f"slide_{sample_idx:02d}.png"),
        )

    if os.path.isdir(OUT_DIR_DL):
        shutil.copy(html_out, os.path.join(OUT_DIR_DL, os.path.basename(html_out)))
        shutil.copy(pptx_out, os.path.join(OUT_DIR_DL, os.path.basename(pptx_out)))
        shutil.copy(pdf_out, os.path.join(OUT_DIR_DL, os.path.basename(pdf_out)))

    print("DONE!")


if __name__ == "__main__":
    main()
