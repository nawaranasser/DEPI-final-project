from flask import Flask, render_template_string, redirect, url_for, request, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mylibrary_secret_key_2024'

# Books data (70 diverse books with enhanced styling)
books = [
    # Self Development (15 books)
    {"id": 1, "title": "Atomic Habits", "author": "James Clear", "price": 220, "category": "Self Development", "description": "An amazing book about building small habits that lead to big changes in life.", "pages": 320, "language": "English", "format": "PDF", "icon": "🌟", "bestseller": True, "color": "#FF6B6B", "gradient": "linear-gradient(135deg, #FF6B6B, #FF8E53)"},
    {"id": 2, "title": "Think and Grow Rich", "author": "Napoleon Hill", "price": 180, "category": "Self Development", "description": "One of the most famous self-development and success books in the world.", "pages": 250, "language": "English", "format": "PDF", "icon": "💎", "bestseller": True, "color": "#4ECDC4", "gradient": "linear-gradient(135deg, #4ECDC4, #44A08D)"},
    {"id": 3, "title": "The Power of Positive Thinking", "author": "Norman Vincent Peale", "price": 200, "category": "Self Development", "description": "Learn how to use the power of positive thinking to change your life.", "pages": 280, "language": "English", "format": "EPUB", "icon": "⚡", "bestseller": False, "color": "#45B7D1", "gradient": "linear-gradient(135deg, #45B7D1, #96C93D)"},
    {"id": 4, "title": "The 7 Habits of Highly Effective People", "author": "Stephen Covey", "price": 240, "category": "Self Development", "description": "Powerful lessons in personal change and effectiveness.", "pages": 380, "language": "English", "format": "PDF", "icon": "🔑", "bestseller": True, "color": "#FAD961", "gradient": "linear-gradient(135deg, #FAD961, #F76B1C)"},
    {"id": 5, "title": "How to Win Friends and Influence People", "author": "Dale Carnegie", "price": 190, "category": "Self Development", "description": "Timeless advice on building relationships and influence.", "pages": 320, "language": "English", "format": "EPUB", "icon": "🤝", "bestseller": True, "color": "#A8E6CF", "gradient": "linear-gradient(135deg, #A8E6CF, #56AB2F)"},
    {"id": 6, "title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson", "price": 210, "category": "Self Development", "description": "A counterintuitive approach to living a good life.", "pages": 240, "language": "English", "format": "PDF", "icon": "🌀", "bestseller": True, "color": "#FFD3B6", "gradient": "linear-gradient(135deg, #FFD3B6, #FFAAA5)"},
    {"id": 7, "title": "Mindset: The New Psychology of Success", "author": "Carol Dweck", "price": 230, "category": "Self Development", "description": "How we can learn to fulfill our potential through growth mindset.", "pages": 320, "language": "English", "format": "EPUB", "icon": "🧠", "bestseller": False, "color": "#D4A5A5", "gradient": "linear-gradient(135deg, #D4A5A5, #FF968A)"},
    {"id": 8, "title": "Deep Work", "author": "Cal Newport", "price": 220, "category": "Self Development", "description": "Rules for focused success in a distracted world.", "pages": 300, "language": "English", "format": "PDF", "icon": "🎯", "bestseller": True, "color": "#96CEB4", "gradient": "linear-gradient(135deg, #96CEB4, #FFEEAD)"},
    {"id": 9, "title": "The 5 AM Club", "author": "Robin Sharma", "price": 240, "category": "Self Development", "description": "Own your morning, elevate your life.", "pages": 350, "language": "English", "format": "EPUB", "icon": "🌅", "bestseller": False, "color": "#FFEAA7", "gradient": "linear-gradient(135deg, #FFEAA7, #DDA15E)"},
    {"id": 10, "title": "Emotional Intelligence", "author": "Daniel Goleman", "price": 260, "category": "Self Development", "description": "Why EQ matters more than IQ.", "pages": 380, "language": "English", "format": "PDF", "icon": "❤️", "bestseller": True, "color": "#DDA15E", "gradient": "linear-gradient(135deg, #DDA15E, #BC6C25)"},

    # Business & Entrepreneurship (15 books)
    {"id": 11, "title": "The Lean Startup", "author": "Eric Ries", "price": 280, "category": "Business & Entrepreneurship", "description": "How to build a successful company using agile development methodology.", "pages": 300, "language": "English", "format": "PDF", "icon": "🚀", "bestseller": True, "color": "#6A0572", "gradient": "linear-gradient(135deg, #6A0572, #AB83A1)"},
    {"id": 12, "title": "Zero to One", "author": "Peter Thiel", "price": 300, "category": "Business & Entrepreneurship", "description": "How to build the future through innovation and monopoly.", "pages": 220, "language": "English", "format": "EPUB", "icon": "💎", "bestseller": True, "color": "#118AB2", "gradient": "linear-gradient(135deg, #118AB2, #06D6A0)"},
    {"id": 13, "title": "Good to Great", "author": "Jim Collins", "price": 290, "category": "Business & Entrepreneurship", "description": "Why some companies make the leap and others don't.", "pages": 320, "language": "English", "format": "EPUB", "icon": "📈", "bestseller": True, "color": "#EF476F", "gradient": "linear-gradient(135deg, #EF476F, #FFD166)"},
    {"id": 14, "title": "Start with Why", "author": "Simon Sinek", "price": 270, "category": "Business & Entrepreneurship", "description": "How great leaders inspire everyone to take action.", "pages": 260, "language": "English", "format": "PDF", "icon": "🎯", "bestseller": False, "color": "#073B4C", "gradient": "linear-gradient(135deg, #073B4C, #118AB2)"},
    {"id": 15, "title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "price": 250, "category": "Business & Entrepreneurship", "description": "What the rich teach their kids about money.", "pages": 270, "language": "English", "format": "PDF", "icon": "💰", "bestseller": True, "color": "#FFD166", "gradient": "linear-gradient(135deg, #FFD166, #EF476F)"},

    # Programming & Technology (20 books)
    {"id": 21, "title": "Learn Python in 30 Days", "author": "Ahmed Mohamed", "price": 350, "category": "Programming & Technology", "description": "Comprehensive course to learn Python from beginner to professional.", "pages": 350, "language": "English", "format": "PDF", "icon": "🐍", "bestseller": True, "color": "#377771", "gradient": "linear-gradient(135deg, #377771, #8EE3EF)"},
    {"id": 22, "title": "Advanced HTML5 & CSS3", "author": "Mohamed Ali", "price": 320, "category": "Programming & Technology", "description": "Learn the latest frontend development technologies.", "pages": 320, "language": "English", "format": "EPUB", "icon": "🌐", "bestseller": False, "color": "#254E70", "gradient": "linear-gradient(135deg, #254E70, #8EE3EF)"},
    {"id": 23, "title": "Modern JavaScript", "author": "Sarah Al-Khaled", "price": 380, "category": "Programming & Technology", "description": "Master JavaScript with the latest features and additions.", "pages": 380, "language": "English", "format": "PDF", "icon": "⚡", "bestseller": True, "color": "#F4A261", "gradient": "linear-gradient(135deg, #F4A261, #E76F51)"},
    {"id": 24, "title": "Learn React from Scratch", "author": "Khaled Ahmed", "price": 400, "category": "Programming & Technology", "description": "Complete guide to learning React.js framework.", "pages": 400, "language": "English", "format": "EPUB", "icon": "⚛️", "bestseller": True, "color": "#61DAFB", "gradient": "linear-gradient(135deg, #61DAFB, #2C5530)"},
    {"id": 25, "title": "Node.js for Beginners", "author": "Fatima Mohamed", "price": 360, "category": "Programming & Technology", "description": "Learn server programming using Node.js.", "pages": 340, "language": "English", "format": "PDF", "icon": "🟢", "bestseller": False, "color": "#8FBC8F", "gradient": "linear-gradient(135deg, #8FBC8F, #2C5530)"},

    # Literature & Novels (20 books)
    {"id": 31, "title": "1984", "author": "George Orwell", "price": 240, "category": "Literature & Novels", "description": "Classic dystopian novel about totalitarian regime.", "pages": 350, "language": "English", "format": "PDF", "icon": "🏘️", "bestseller": True, "color": "#2A2D34", "gradient": "linear-gradient(135deg, #2A2D34, #5C6BC0)"},
    {"id": 32, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 220, "category": "Literature & Novels", "description": "Classic American novel about racial injustice.", "pages": 320, "language": "English", "format": "EPUB", "icon": "🐦", "bestseller": True, "color": "#6D6875", "gradient": "linear-gradient(135deg, #6D6875, #E5989B)"},
    {"id": 33, "title": "The Alchemist", "author": "Paulo Coelho", "price": 200, "category": "Literature & Novels", "description": "Philosophical novel about self-discovery and achieving dreams.", "pages": 200, "language": "English", "format": "PDF", "icon": "🧙", "bestseller": True, "color": "#FFB4A2", "gradient": "linear-gradient(135deg, #FFB4A2, #E5989B)"},
    {"id": 34, "title": "Pride and Prejudice", "author": "Jane Austen", "price": 210, "category": "Literature & Novels", "description": "Classic romance novel about manners and marriage.", "pages": 430, "language": "English", "format": "PDF", "icon": "💕", "bestseller": False, "color": "#B5838D", "gradient": "linear-gradient(135deg, #B5838D, #6D6875)"},
    {"id": 35, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 190, "category": "Literature & Novels", "description": "American classic about the Jazz Age and American Dream.", "pages": 180, "language": "English", "format": "EPUB", "icon": "🎭", "bestseller": True, "color": "#FFCDB2", "gradient": "linear-gradient(135deg, #FFCDB2, #FFB4A2)"},
]

# Book categories
categories = list(set([b["category"] for b in books]))

# Cart and Library
cart = []
library = []

# Enhanced CSS styles
enhanced_styles = '''
<style>
    :root {
        --primary: #2C5530;
        --secondary: #4A7C59;
        --accent: #8FBC8F;
        --light: #F8F9FA;
        --dark: #1A1A1A;
        --gold: #D4AF37;
        --cream: #FFF8F0;
        --navy: #1E3A5F;
        --luxury-gold: #C9A96E;
        --deep-navy: #0A1A2F;
        --emerald: #2E8B57;
        --ruby: #E0115F;
        --sapphire: #0F52BA;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #0A1A2F 0%, #1E3A5F 50%, #2C5530 100%);
        color: white;
        line-height: 1.6;
        overflow-x: hidden;
        min-height: 100vh;
    }
    
    .luxury-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(201, 169, 110, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(46, 139, 87, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, #0A1A2F 0%, #1E3A5F 100%);
        z-index: -2;
    }
    
    .gold-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, 
            transparent 0%, 
            rgba(201, 169, 110, 0.03) 50%, 
            transparent 100%);
        z-index: -1;
        animation: shimmer 8s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.7; }
    }
    
    header {
        background: rgba(10, 26, 47, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(201, 169, 110, 0.2);
        padding: 1rem 0;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo {
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'Playfair Display', 'Times New Roman', serif;
        background: linear-gradient(135deg, var(--luxury-gold), #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(201, 169, 110, 0.3);
    }
    
    .logo-icon {
        font-size: 3rem;
        animation: gentleFloat 4s ease-in-out infinite;
        filter: drop-shadow(0 4px 8px rgba(201, 169, 110, 0.4));
    }
    
    @keyframes gentleFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-5px) rotate(2deg); }
        66% { transform: translateY(3px) rotate(-1deg); }
    }
    
    nav ul {
        display: flex;
        list-style: none;
        gap: 1.5rem;
        align-items: center;
    }
    
    nav a {
        color: rgba(255, 255, 255, 0.9);
        text-decoration: none;
        font-weight: 500;
        font-size: 1.1rem;
        padding: 0.8rem 1.8rem;
        border-radius: 15px;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(201, 169, 110, 0.3);
        background: rgba(255, 255, 255, 0.05);
    }
    
    nav a::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        z-index: -1;
        opacity: 0;
    }
    
    nav a:hover::before {
        left: 0;
        opacity: 1;
    }
    
    nav a:hover {
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(201, 169, 110, 0.3);
        border-color: transparent;
    }
    
    .cart-count, .library-count {
        background: linear-gradient(135deg, var(--ruby), #FF6B6B);
        color: white;
        border-radius: 50%;
        padding: 0.3rem 0.7rem;
        font-size: 0.8rem;
        margin-left: 0.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(224, 17, 95, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .hero {
        text-align: center;
        padding: 8rem 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(201, 169, 110, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(46, 139, 87, 0.15) 0%, transparent 50%);
        z-index: 0;
    }
    
    .hero-content {
        max-width: 900px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    
    .hero h1 {
        font-size: 4.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #FFFFFF, var(--luxury-gold));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        line-height: 1.2;
        letter-spacing: -0.5px;
    }
    
    .hero p {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .search-bar {
        max-width: 600px;
        margin: 3rem auto;
        position: relative;
    }
    
    .search-bar input {
        width: 100%;
        padding: 1.4rem 3rem 1.4rem 2rem;
        border: 2px solid rgba(201, 169, 110, 0.3);
        border-radius: 50px;
        font-size: 1.1rem;
        outline: none;
        transition: all 0.4s ease;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .search-bar input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .search-bar input:focus {
        border-color: var(--luxury-gold);
        box-shadow: 0 8px 32px rgba(201, 169, 110, 0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
        color: var(--deep-navy);
        padding: 1.4rem 3rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        border: none;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(201, 169, 110, 0.4);
        font-size: 1.1rem;
        position: relative;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
    }
    
    .btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--emerald), var(--luxury-gold));
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        z-index: -1;
    }
    
    .btn:hover::before {
        left: 0;
    }
    
    .btn:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 40px rgba(201, 169, 110, 0.6);
        color: var(--deep-navy);
    }
    
    .btn-outline {
        background: transparent;
        border: 2px solid var(--luxury-gold);
        color: var(--luxury-gold);
        box-shadow: none;
    }
    
    .btn-outline:hover {
        background: var(--luxury-gold);
        color: var(--deep-navy);
    }
    
    .section-title {
        text-align: center;
        margin-bottom: 4rem;
        position: relative;
    }
    
    .section-title h2 {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #FFFFFF, var(--luxury-gold));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        display: inline-block;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .section-title h2::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
        border-radius: 2px;
        box-shadow: 0 2px 10px rgba(201, 169, 110, 0.4);
    }
    
    .bestsellers {
        padding: 6rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .books-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 3rem;
        margin-bottom: 4rem;
    }
    
    .book-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .book-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: var(--book-gradient, linear-gradient(135deg, var(--luxury-gold), var(--emerald)));
    }
    
    .book-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .bestseller-badge {
        position: absolute;
        top: 25px;
        right: 25px;
        background: linear-gradient(135deg, var(--ruby), #FF6B6B);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(224, 17, 95, 0.4);
        z-index: 2;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 4px 15px rgba(224, 17, 95, 0.4); }
        to { box-shadow: 0 6px 20px rgba(224, 17, 95, 0.6); }
    }
    
    .book-icon {
        font-size: 5rem;
        margin-bottom: 2rem;
        display: block;
        filter: drop-shadow(0 6px 12px rgba(0,0,0,0.3));
        animation: iconFloat 3s ease-in-out infinite;
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-8px) rotate(5deg); }
        66% { transform: translateY(4px) rotate(-3deg); }
    }
    
    .book-category {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1.5rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .book-title {
        font-size: 1.6rem;
        margin-bottom: 1rem;
        color: white;
        font-weight: 700;
        line-height: 1.4;
        font-family: 'Playfair Display', serif;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .book-author {
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1.5rem;
        font-style: italic;
        font-size: 1.1rem;
    }
    
    .book-details {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        padding: 0 1rem;
    }
    
    .book-price {
        color: var(--luxury-gold);
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-shadow: 0 2px 10px rgba(201, 169, 110, 0.4);
    }
    
    .currency {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .categories {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin: 4rem auto;
        max-width: 1200px;
        padding: 0 2rem;
    }
    
    .category-btn {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(201, 169, 110, 0.3);
        padding: 1.2rem 2.5rem;
        border-radius: 50px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.4s ease;
        color: rgba(255, 255, 255, 0.9);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        font-size: 1rem;
    }
    
    .category-btn.active, .category-btn:hover {
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
        color: var(--deep-navy);
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(201, 169, 110, 0.4);
        border-color: transparent;
    }
    
    .features {
        padding: 6rem 2rem;
        background: rgba(255, 255, 255, 0.05);
        margin-top: 4rem;
        border-top: 1px solid rgba(201, 169, 110, 0.2);
        border-bottom: 1px solid rgba(201, 169, 110, 0.2);
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 3rem 2.5rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 50px rgba(0,0,0,0.3);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 2rem;
        display: block;
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .feature-card h3 {
        font-size: 1.6rem;
        margin-bottom: 1.5rem;
        color: white;
        font-family: 'Playfair Display', serif;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .feature-card p {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.7;
        font-size: 1.1rem;
    }
    
    footer {
        background: linear-gradient(135deg, var(--deep-navy), #051322);
        color: white;
        padding: 5rem 2rem 3rem;
        margin-top: 6rem;
        border-top: 1px solid rgba(201, 169, 110, 0.2);
    }
    
    .footer-content {
        max-width: 1400px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 4rem;
    }
    
    .footer-section h3 {
        margin-bottom: 2rem;
        font-size: 1.6rem;
        position: relative;
        display: inline-block;
        font-family: 'Playfair Display', serif;
        background: linear-gradient(135deg, var(--luxury-gold), white);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer-section h3::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
        border-radius: 2px;
    }
    
    .footer-section p {
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    
    .footer-section ul {
        list-style: none;
    }
    
    .footer-section li {
        margin-bottom: 1rem;
    }
    
    .footer-section a {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .footer-section a:hover {
        color: var(--luxury-gold);
        padding-left: 8px;
    }
    
    .copyright {
        margin-top: 5rem;
        padding-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.5);
        text-align: center;
        font-size: 0.9rem;
    }
    
    .social-links {
        display: flex;
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .social-links a {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        transition: all 0.4s ease;
        border: 1px solid rgba(201, 169, 110, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .social-links a:hover {
        background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 10px 25px rgba(201, 169, 110, 0.4);
    }
    
    @media (max-width: 768px) {
        .header-content {
            flex-direction: column;
            gap: 1.5rem;
            padding: 0 1rem;
        }
        
        nav ul {
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        nav a {
            font-size: 1rem;
            padding: 0.7rem 1.2rem;
        }
        
        .hero h1 {
            font-size: 3rem;
        }
        
        .hero p {
            font-size: 1.2rem;
        }
        
        .books-grid {
            grid-template-columns: 1fr;
            gap: 2.5rem;
        }
        
        .section-title h2 {
            font-size: 2.5rem;
        }
        
        .categories {
            gap: 1rem;
        }
        
        .category-btn {
            padding: 1rem 2rem;
            font-size: 0.9rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero {
            padding: 6rem 1rem;
        }
        
        .hero h1 {
            font-size: 2.2rem;
        }
        
        .logo {
            font-size: 1.8rem;
        }
        
        .logo-icon {
            font-size: 2.5rem;
        }
        
        .footer-content {
            grid-template-columns: 1fr;
            text-align: center;
            gap: 3rem;
        }
        
        .footer-section h3::after {
            left: 50%;
            transform: translateX(-50%);
        }
        
        .social-links {
            justify-content: center;
        }
    }
</style>
'''

# Home Page
@app.route('/')
def home():
    # Get bestseller books
    bestsellers = [book for book in books if book.get('bestseller', False)][:8]
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📚 MyLibrary - Premium E-Book Store</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        {enhanced_styles}
    </head>
    <body>
        <div class="luxury-bg"></div>
        <div class="gold-overlay"></div>
        
        <header>
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📚</span>
                    <span>MyLibrary</span>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/all-books">All Books</a></li>
                        <li><a href="/cart">Cart <span class="cart-count">{len(cart)}</span></a></li>
                        <li><a href="/library">My Library <span class="library-count">{len(library)}</span></a></li>
                        <li><a href="/about">About</a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <section class="hero">
            <div class="hero-content">
                <h1>Discover Your Next<br>Masterpiece</h1>
                <p>Premium e-books for the discerning reader • Instant delivery • Exclusive collection</p>
                
                <div class="search-bar">
                    <input type="text" id="searchInput" placeholder="Search for books, authors, or topics...">
                </div>
                
                <a href="#bestsellers" class="btn">
                    <span>Explore Masterpieces</span>
                    <span>✨</span>
                </a>
            </div>
        </section>
        
        <section class="bestsellers" id="bestsellers">
            <div class="section-title">
                <h2>Featured Masterpieces</h2>
            </div>
            
            <div class="books-grid">
                {"".join([f'''
                <div class="book-card" style="--book-gradient: {book['gradient']}">
                    {"<div class='bestseller-badge'>Bestseller</div>" if book.get('bestseller') else ""}
                    <span class="book-icon" style="color: {book['color']}">{book['icon']}</span>
                    <div class="book-category">{book['category']}</div>
                    <h3 class="book-title">{book['title']}</h3>
                    <p class="book-author">By {book['author']}</p>
                    <div class="book-details">
                        <span>📄 {book['pages']} pages</span>
                        <span>📝 {book['format']}</span>
                    </div>
                    <p class="book-price">
                        <span class="currency">EGP</span>
                        {book['price']}
                    </p>
                    <a href="/book/{book['id']}" class="btn">View Details</a>
                </div>
                ''' for book in bestsellers])}
            </div>
        </section>
        
        <div class="categories">
            <button class="category-btn active" onclick="filterBooks('all')">All Collections</button>
            {"".join([f'''<button class="category-btn" onclick="filterBooks('{cat}')">{cat}</button>''' for cat in categories])}
        </div>
        
        <section class="features">
            <div class="section-title">
                <h2>Why Choose MyLibrary?</h2>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Instant Access</h3>
                    <p>Receive your premium e-books immediately after purchase, ready for any device</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💎</div>
                    <h3>Exclusive Collection</h3>
                    <p>Curated selection of the finest books across all genres and categories</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3>Universal Compatibility</h3>
                    <p>Seamless reading experience across all your devices and platforms</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <h3>Secure & Private</h3>
                    <p>Bank-level security with multiple trusted payment options</p>
                </div>
            </div>
        </section>
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>MyLibrary</h3>
                    <p>Egypt's premier destination for premium digital literature, offering an exclusive collection for the modern reader.</p>
                    <div class="social-links">
                        <a href="#">📘</a>
                        <a href="#">🐦</a>
                        <a href="#">📷</a>
                        <a href="#">💼</a>
                    </div>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="/">🏠 Home</a></li>
                        <li><a href="/all-books">📚 All Collections</a></li>
                        <li><a href="/cart">🛒 Shopping Cart</a></li>
                        <li><a href="/library">📖 My Library</a></li>
                        <li><a href="/about">ℹ️ About Us</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <ul>
                        <li><a href="tel:+201234567890">📞 +20 123 456 7890</a></li>
                        <li><a href="mailto:premium@mylibrary.com">✉️ premium@mylibrary.com</a></li>
                        <li><a href="#">📍 Downtown Cairo, Egypt</a></li>
                        <li><a href="#">🕒 Daily 9AM - 10PM</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Premium Newsletter</h3>
                    <p>Subscribe for exclusive offers and new collection notifications</p>
                    <div class="search-bar" style="max-width: 100%; margin: 1.5rem 0;">
                        <input type="email" placeholder="Enter your email...">
                    </div>
                    <button class="btn" style="width: 100%;">Subscribe</button>
                </div>
            </div>
            <div class="copyright">
                <p>© 2024 MyLibrary - Premium Digital Library. Downtown Cairo, Egypt. All Rights Reserved.</p>
            </div>
        </footer>
        
        <script>
            function filterBooks(category) {{
                const books = document.querySelectorAll('.book-card');
                const buttons = document.querySelectorAll('.category-btn');
                
                buttons.forEach(btn => {{
                    if (btn.textContent === category || (category === 'all' && btn.textContent === 'All Collections')) {{
                        btn.classList.add('active');
                    }} else {{
                        btn.classList.remove('active');
                    }}
                }});
                
                books.forEach(book => {{
                    if (category === 'all' || book.querySelector('.book-category').textContent === category) {{
                        book.style.display = 'block';
                    }} else {{
                        book.style.display = 'none';
                    }}
                }});
            }}
            
            // Book search functionality
            document.getElementById('searchInput').addEventListener('input', function(e) {{
                const searchTerm = e.target.value.toLowerCase();
                const books = document.querySelectorAll('.book-card');
                
                books.forEach(book => {{
                    const title = book.querySelector('.book-title').textContent.toLowerCase();
                    const author = book.querySelector('.book-author').textContent.toLowerCase();
                    const category = book.querySelector('.book-category').textContent.toLowerCase();
                    
                    if (title.includes(searchTerm) || author.includes(searchTerm) || category.includes(searchTerm)) {{
                        book.style.display = 'block';
                    }} else {{
                        book.style.display = 'none';
                    }}
                }});
            }});
            
            // Header scroll effect
            window.addEventListener('scroll', function() {{
                const header = document.querySelector('header');
                if (window.scrollY > 100) {{
                    header.style.background = 'rgba(10, 26, 47, 0.98)';
                    header.style.boxShadow = '0 5px 20px rgba(0,0,0,0.3)';
                }} else {{
                    header.style.background = 'rgba(10, 26, 47, 0.95)';
                    header.style.boxShadow = 'none';
                }}
            }});
            
            // Add parallax effect to background
            window.addEventListener('scroll', function() {{
                const scrolled = window.pageYOffset;
                const luxuryBg = document.querySelector('.luxury-bg');
                luxuryBg.style.transform = 'translateY(' + (scrolled * 0.5) + 'px)';
            }});
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, books=books, categories=categories, cart_count=len(cart), 
                                 library_count=len(library), bestsellers=bestsellers)

# All Books Page with enhanced design
@app.route('/all-books')
def all_books():
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Complete Collection - MyLibrary</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        {enhanced_styles}
        <style>
            .page-header {{
                text-align: center;
                padding: 6rem 2rem;
                background: linear-gradient(135deg, rgba(201, 169, 110, 0.1), rgba(46, 139, 87, 0.1));
                position: relative;
                overflow: hidden;
            }}
            
            .page-header h1 {{
                font-size: 4rem;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, #FFFFFF, var(--luxury-gold));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: 'Playfair Display', serif;
                font-weight: 700;
                text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }}
            
            .page-header p {{
                font-size: 1.4rem;
                color: rgba(255, 255, 255, 0.8);
                max-width: 600px;
                margin: 0 auto;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }}
            
            .books-container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 4rem 2rem;
            }}
            
            .books-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 3rem;
            }}
            
            .collection-stats {{
                text-align: center;
                margin-bottom: 3rem;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(201, 169, 110, 0.2);
            }}
            
            .stats-number {{
                font-size: 3rem;
                font-weight: 700;
                background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1rem;
            }}
            
            .stats-label {{
                font-size: 1.2rem;
                color: rgba(255, 255, 255, 0.8);
            }}
        </style>
    </head>
    <body>
        <div class="luxury-bg"></div>
        <div class="gold-overlay"></div>
        
        <header>
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📚</span>
                    <span>MyLibrary</span>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/all-books">All Collections</a></li>
                        <li><a href="/cart">Cart <span class="cart-count">{len(cart)}</span></a></li>
                        <li><a href="/library">My Library <span class="library-count">{len(library)}</span></a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <section class="page-header">
            <h1>Our Complete Collection</h1>
            <p>Discover {len(books)} premium masterpieces across exclusive categories</p>
        </section>
        
        <div class="collection-stats">
            <div class="stats-number">{len(books)}</div>
            <div class="stats-label">Premium Books in Collection</div>
        </div>
        
        <div class="categories">
            <button class="category-btn active" onclick="filterBooks('all')">All Collections</button>
            {"".join([f'''<button class="category-btn" onclick="filterBooks('{cat}')">{cat}</button>''' for cat in categories])}
        </div>
        
        <div class="books-container">
            <div class="books-grid">
                {"".join([f'''
                <div class="book-card" data-category="{book['category']}" style="--book-gradient: {book['gradient']}">
                    {"<div class='bestseller-badge'>Bestseller</div>" if book.get('bestseller') else ""}
                    <span class="book-icon" style="color: {book['color']}">{book['icon']}</span>
                    <div class="book-category">{book['category']}</div>
                    <h3 class="book-title">{book['title']}</h3>
                    <p class="book-author">By {book['author']}</p>
                    <div class="book-details">
                        <span>📄 {book['pages']} pages</span>
                        <span>📝 {book['format']}</span>
                    </div>
                    <p class="book-price">
                        <span class="currency">EGP</span>
                        {book['price']}
                    </p>
                    <a href="/book/{book['id']}" class="btn">View Details</a>
                </div>
                ''' for book in books])}
            </div>
        </div>
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>MyLibrary</h3>
                    <p>Egypt's premier destination for premium digital literature.</p>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>📞 +20 123 456 7890</p>
                    <p>✉️ premium@mylibrary.com</p>
                    <p>📍 Downtown Cairo, Egypt</p>
                </div>
            </div>
            <div class="copyright">
                <p>© 2024 MyLibrary - Premium Digital Library. Downtown Cairo, Egypt. All Rights Reserved.</p>
            </div>
        </footer>
        
        <script>
            function filterBooks(category) {{
                const books = document.querySelectorAll('.book-card');
                const buttons = document.querySelectorAll('.category-btn');
                
                buttons.forEach(btn => {{
                    if (btn.textContent === category || (category === 'all' && btn.textContent === 'All Collections')) {{
                        btn.classList.add('active');
                    }} else {{
                        btn.classList.remove('active');
                    }}
                }});
                
                books.forEach(book => {{
                    if (category === 'all' || book.dataset.category === category) {{
                        book.style.display = 'block';
                    }} else {{
                        book.style.display = 'none';
                    }}
                }});
            }}
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, books=books, categories=categories, cart_count=len(cart), library_count=len(library))

# Book Details Page with enhanced design
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return "Book not found"
    
    # Get related books (same category)
    related_books = [b for b in books if b["category"] == book["category"] and b["id"] != book["id"]][:4]
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{book['title']} - MyLibrary</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        {enhanced_styles}
        <style>
            .book-detail {{
                max-width: 1300px;
                margin: 3rem auto;
                padding: 0 2rem;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4rem;
                align-items: start;
            }}
            
            .book-cover {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 30px;
                padding: 4rem 3rem;
                text-align: center;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
            }}
            
            .book-cover::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 6px;
                background: {book['gradient']};
            }}
            
            .book-icon-large {{
                font-size: 10rem;
                display: block;
                margin-bottom: 3rem;
                color: {book['color']};
                filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
                animation: iconFloatLarge 4s ease-in-out infinite;
            }}
            
            @keyframes iconFloatLarge {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg) scale(1); }}
                33% {{ transform: translateY(-15px) rotate(8deg) scale(1.05); }}
                66% {{ transform: translateY(8px) rotate(-4deg) scale(0.95); }}
            }}
            
            .book-info {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 30px;
                padding: 4rem 3rem;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                position: relative;
            }}
            
            .book-info::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 6px;
                background: {book['gradient']};
            }}
            
            .book-title {{
                font-size: 3rem;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, #FFFFFF, {book['color']});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.2;
                font-family: 'Playfair Display', serif;
                font-weight: 700;
                text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }}
            
            .book-author {{
                font-size: 1.6rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 2.5rem;
                font-style: italic;
            }}
            
            .book-price {{
                color: var(--luxury-gold);
                font-weight: 700;
                font-size: 3.5rem;
                margin-bottom: 2.5rem;
                display: flex;
                align-items: center;
                gap: 10px;
                text-shadow: 0 2px 15px rgba(201, 169, 110, 0.5);
            }}
            
            .currency {{
                font-size: 2rem;
                color: rgba(255, 255, 255, 0.8);
            }}
            
            .book-meta {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
                margin-bottom: 3rem;
                padding: 2.5rem;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .meta-item {{
                display: flex;
                align-items: center;
                gap: 1.5rem;
                font-size: 1.2rem;
                color: rgba(255, 255, 255, 0.9);
            }}
            
            .meta-item span:first-child {{
                font-size: 1.8rem;
            }}
            
            .book-description {{
                margin-bottom: 3rem;
                line-height: 1.8;
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.2rem;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                border-left: 4px solid {book['color']};
            }}
            
            .book-actions {{
                display: flex;
                gap: 1.5rem;
                flex-wrap: wrap;
            }}
            
            .btn-large {{
                padding: 1.5rem 3rem;
                font-size: 1.2rem;
            }}
            
            .related-books {{
                max-width: 1300px;
                margin: 6rem auto;
                padding: 0 2rem;
            }}
            
            @media (max-width: 968px) {{
                .book-detail {{
                    grid-template-columns: 1fr;
                    gap: 3rem;
                }}
                
                .book-title {{
                    font-size: 2.2rem;
                }}
                
                .book-meta {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="luxury-bg"></div>
        <div class="gold-overlay"></div>
        
        <header>
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📚</span>
                    <span>MyLibrary</span>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/all-books">All Collections</a></li>
                        <li><a href="/cart">Cart</a></li>
                        <li><a href="/library">My Library</a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <div class="book-detail">
            <div class="book-cover">
                <span class="book-icon-large">{book['icon']}</span>
                <div class="book-category">{book['category']}</div>
                {"<div style='background: linear-gradient(135deg, var(--ruby), #FF6B6B); color: white; padding: 1rem 2rem; border-radius: 25px; font-size: 1rem; font-weight: 600; display: inline-block; margin-top: 2rem; box-shadow: 0 4px 15px rgba(224, 17, 95, 0.4); animation: glow 2s ease-in-out infinite alternate;'>⭐ Premium Bestseller</div>" if book.get('bestseller') else ""}
            </div>
            <div class="book-info">
                <h1 class="book-title">{book['title']}</h1>
                <p class="book-author">By {book['author']}</p>
                <p class="book-price">
                    <span class="currency">EGP</span>
                    {book['price']}
                </p>
                
                <div class="book-meta">
                    <div class="meta-item">
                        <span>📄</span>
                        <span>{book['pages']} premium pages</span>
                    </div>
                    <div class="meta-item">
                        <span>📝</span>
                        <span>Format: {book['format']}</span>
                    </div>
                    <div class="meta-item">
                        <span>🌐</span>
                        <span>Language: {book['language']}</span>
                    </div>
                    <div class="meta-item">
                        <span>📚</span>
                        <span>Collection: {book['category']}</span>
                    </div>
                </div>
                
                <div class="book-description">
                    <p>{book['description']}</p>
                </div>
                
                <div class="book-actions">
                    <a href="/add_to_cart/{book['id']}" class="btn btn-large">
                        <span>🛒 Add to Collection</span>
                    </a>
                    <a href="/all-books" class="btn btn-large btn-outline">
                        <span>← Back to Collections</span>
                    </a>
                </div>
            </div>
        </div>
        
        {"".join([f'''
        <section class="related-books">
            <div class="section-title">
                <h2>Related Masterpieces</h2>
            </div>
            <div class="books-grid">
                {"".join([f'''
                <div class="book-card" style="--book-gradient: {related_book['gradient']}">
                    <span class="book-icon" style="color: {related_book['color']}">{related_book['icon']}</span>
                    <div class="book-category">{related_book['category']}</div>
                    <h3 class="book-title">{related_book['title']}</h3>
                    <p class="book-author">By {related_book['author']}</p>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem; font-size: 0.9rem; color: rgba(255, 255, 255, 0.7); padding: 0 1rem;">
                        <span>📄 {related_book['pages']}p</span>
                        <span>📝 {related_book['format']}</span>
                    </div>
                    <p class="book-price">
                        <span class="currency">EGP</span>
                        {related_book['price']}
                    </p>
                    <a href="/book/{related_book['id']}" class="btn">Explore</a>
                </div>
                ''' for related_book in related_books])}
            </div>
        </section>
        ''']) if related_books else ''}
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>MyLibrary</h3>
                    <p>Egypt's premier destination for premium digital literature.</p>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>📞 +20 123 456 7890</p>
                    <p>✉️ premium@mylibrary.com</p>
                    <p>📍 Downtown Cairo, Egypt</p>
                </div>
            </div>
            <div class="copyright">
                <p>© 2024 MyLibrary - Premium Digital Library. Downtown Cairo, Egypt. All Rights Reserved.</p>
            </div>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html, book=book, related_books=related_books)

# Add to Cart
@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        # Check if book already exists in cart
        for item in cart:
            if item["id"] == book_id:
                return redirect(url_for('cart_view'))
        else:
            book_with_quantity = book.copy()
            book_with_quantity["quantity"] = 1
            cart.append(book_with_quantity)
    return redirect(url_for('cart_view'))

# Remove from Cart
@app.route('/remove_from_cart/<int:book_id>')
def remove_from_cart(book_id):
    global cart
    cart = [item for item in cart if item["id"] != book_id]
    return redirect(url_for('cart_view'))

# Cart Page
@app.route('/cart')
def cart_view():
    total = sum(b["price"] * b["quantity"] for b in cart)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Premium Collection Cart - MyLibrary</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        {enhanced_styles}
        <style>
            .cart-container {{
                max-width: 1200px;
                margin: 3rem auto;
                padding: 0 2rem;
            }}
            
            .cart-title {{
                text-align: center;
                margin-bottom: 4rem;
                font-size: 3.5rem;
                background: linear-gradient(135deg, #FFFFFF, var(--luxury-gold));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: 'Playfair Display', serif;
                font-weight: 700;
                text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }}
            
            .cart-table {{
                width: 100%;
                border-collapse: collapse;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                overflow: hidden;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                margin-bottom: 3rem;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .cart-table th {{
                background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
                color: var(--deep-navy);
                padding: 2rem;
                text-align: left;
                font-weight: 600;
                font-size: 1.2rem;
            }}
            
            .cart-table td {{
                padding: 2rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                vertical-align: middle;
                color: rgba(255, 255, 255, 0.9);
            }}
            
            .cart-table tr:last-child td {{
                border-bottom: none;
            }}
            
            .item-icon {{
                font-size: 3rem;
                margin-right: 1.5rem;
            }}
            
            .empty-cart {{
                text-align: center;
                padding: 6rem 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 30px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin: 2rem 0;
            }}
            
            .empty-cart-icon {{
                font-size: 8rem;
                margin-bottom: 3rem;
                display: block;
                background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gentleFloat 4s ease-in-out infinite;
            }}
            
            .cart-summary {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                padding: 3rem;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                text-align: center;
                margin-top: 3rem;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .total-price {{
                font-size: 2.8rem;
                font-weight: 700;
                color: var(--luxury-gold);
                margin-bottom: 2.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                text-shadow: 0 2px 15px rgba(201, 169, 110, 0.5);
            }}
            
            .currency {{
                font-size: 2rem;
                color: rgba(255, 255, 255, 0.8);
            }}
            
            .cart-actions {{
                display: flex;
                justify-content: center;
                gap: 2rem;
                flex-wrap: wrap;
            }}
            
            @media (max-width: 768px) {{
                .cart-table {{
                    display: block;
                    overflow-x: auto;
                }}
                
                .cart-actions {{
                    flex-direction: column;
                    align-items: center;
                }}
                
                .btn {{
                    width: 100%;
                    max-width: 300px;
                    justify-content: center;
                }}
                
                .cart-title {{
                    font-size: 2.5rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="luxury-bg"></div>
        <div class="gold-overlay"></div>
        
        <header>
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📚</span>
                    <span>MyLibrary</span>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/all-books">All Collections</a></li>
                        <li><a href="/cart">Cart <span class="cart-count">{len(cart)}</span></a></li>
                        <li><a href="/library">My Library</a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <div class="cart-container">
            <h1 class="cart-title">🛒 Premium Collection</h1>
            
            {"".join([f'''
            <table class="cart-table">
                <thead>
                    <tr>
                        <th>Masterpiece</th>
                        <th>Investment</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f'''
                    <tr>
                        <td style="display: flex; align-items: center;">
                            <span class="item-icon" style="color: {item['color']}">{item['icon']}</span>
                            <div>
                                <strong style="font-size: 1.4rem; color: white;">{item['title']}</strong>
                                <br>
                                <small style="color: rgba(255, 255, 255, 0.7);">By {item['author']}</small>
                            </div>
                        </td>
                        <td style="font-size: 1.6rem; font-weight: 600; color: var(--luxury-gold);">
                            EGP {item['price']}
                        </td>
                        <td>
                            <a href="/remove_from_cart/{item['id']}" class="btn btn-outline">Remove</a>
                        </td>
                    </tr>
                    ''' for item in cart])}
                </tbody>
            </table>
            
            <div class="cart-summary">
                <div class="total-price">
                    <span class="currency">EGP</span>
                    {total}
                </div>
                <div class="cart-actions">
                    <a href="/all-books" class="btn btn-outline">Continue Exploring</a>
                    <a href="/checkout" class="btn">Complete Collection</a>
                </div>
            </div>
            ''']) if cart else f'''
            <div class="empty-cart">
                <span class="empty-cart-icon">📚</span>
                <h2 style="font-size: 2.5rem; color: white; margin-bottom: 1.5rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">Your collection is empty</h2>
                <p style="font-size: 1.3rem; color: rgba(255, 255, 255, 0.8); margin-bottom: 3rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">You haven't added any masterpieces to your collection yet</p>
                <a href="/all-books" class="btn">Explore Masterpieces</a>
            </div>
            '''}
        </div>
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>MyLibrary</h3>
                    <p>Egypt's premier destination for premium digital literature.</p>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>📞 +20 123 456 7890</p>
                    <p>✉️ premium@mylibrary.com</p>
                    <p>📍 Downtown Cairo, Egypt</p>
                </div>
            </div>
            <div class="copyright">
                <p>© 2024 MyLibrary - Premium Digital Library. Downtown Cairo, Egypt. All Rights Reserved.</p>
            </div>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html, cart=cart, total=total, cart_count=len(cart))

# Checkout Page
@app.route('/checkout')
def checkout():
    if not cart:
        return redirect(url_for('cart_view'))
    
    total = sum(b["price"] * b["quantity"] for b in cart)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Secure Checkout - MyLibrary</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        {enhanced_styles}
        <style>
            .checkout-container {{
                max-width: 1200px;
                margin: 3rem auto;
                padding: 0 2rem;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4rem;
            }}
            
            .checkout-title {{
                text-align: center;
                margin-bottom: 4rem;
                font-size: 3.5rem;
                background: linear-gradient(135deg, #FFFFFF, var(--luxury-gold));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: 'Playfair Display', serif;
                font-weight: 700;
                text-shadow: 0 4px 20px rgba(0,0,0,0.3);
                grid-column: 1 / -1;
            }}
            
            .checkout-section {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                padding: 3rem;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                position: relative;
            }}
            
            .checkout-section::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 6px;
                background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
            }}
            
            .section-title {{
                font-size: 1.8rem;
                margin-bottom: 2rem;
                color: white;
                font-family: 'Playfair Display', serif;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }}
            
            .form-group {{
                margin-bottom: 2rem;
            }}
            
            .form-group label {{
                display: block;
                margin-bottom: 0.8rem;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 500;
            }}
            
            .form-control {{
                width: 100%;
                padding: 1.2rem 1.5rem;
                border: 2px solid rgba(201, 169, 110, 0.3);
                border-radius: 15px;
                font-size: 1rem;
                outline: none;
                transition: all 0.4s ease;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                color: white;
            }}
            
            .form-control:focus {{
                border-color: var(--luxury-gold);
                box-shadow: 0 0 0 3px rgba(201, 169, 110, 0.2);
                background: rgba(255, 255, 255, 0.15);
            }}
            
            .payment-methods {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1.5rem;
                margin-bottom: 2rem;
            }}
            
            .payment-method {{
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(201, 169, 110, 0.3);
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .payment-method:hover {{
                border-color: var(--luxury-gold);
                background: rgba(255, 255, 255, 0.1);
            }}
            
            .payment-method.selected {{
                border-color: var(--luxury-gold);
                background: rgba(201, 169, 110, 0.1);
            }}
            
            .payment-icon {{
                font-size: 3rem;
                margin-bottom: 1rem;
                display: block;
            }}
            
            .order-summary {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                padding: 2rem;
                margin-bottom: 2rem;
            }}
            
            .order-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .order-item:last-child {{
                border-bottom: none;
            }}
            
            .order-total {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 2rem 0;
                border-top: 2px solid rgba(255, 255, 255, 0.2);
                font-size: 1.4rem;
                font-weight: 700;
                color: var(--luxury-gold);
            }}
            
            .security-badge {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 1rem;
                padding: 1.5rem;
                background: rgba(46, 139, 87, 0.2);
                border-radius: 15px;
                border: 1px solid rgba(46, 139, 87, 0.3);
                margin-top: 2rem;
                color: rgba(255, 255, 255, 0.9);
            }}
            
            @media (max-width: 968px) {{
                .checkout-container {{
                    grid-template-columns: 1fr;
                    gap: 3rem;
                }}
                
                .payment-methods {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="luxury-bg"></div>
        <div class="gold-overlay"></div>
        
        <header>
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📚</span>
                    <span>MyLibrary</span>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/all-books">All Collections</a></li>
                        <li><a href="/cart">Cart <span class="cart-count">{len(cart)}</span></a></li>
                        <li><a href="/library">My Library</a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <div class="checkout-container">
            <h1 class="checkout-title">Secure Checkout</h1>
            
            <div class="checkout-section">
                <h2 class="section-title">Personal Information</h2>
                <form id="checkoutForm" action="/process_payment" method="POST">
                    <div class="form-group">
                        <label for="fullName">Full Name</label>
                        <input type="text" id="fullName" name="fullName" class="form-control" placeholder="Enter your full name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email" class="form-control" placeholder="Enter your email" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number</label>
                        <input type="tel" id="phone" name="phone" class="form-control" placeholder="Enter your phone number" required>
                    </div>
                    
                    <h2 class="section-title" style="margin-top: 3rem;">Payment Method</h2>
                    <div class="payment-methods">
                        <div class="payment-method" onclick="selectPayment('credit')">
                            <span class="payment-icon">💳</span>
                            <div>Credit Card</div>
                        </div>
                        <div class="payment-method" onclick="selectPayment('paypal')">
                            <span class="payment-icon">🅿️</span>
                            <div>PayPal</div>
                        </div>
                        <div class="payment-method" onclick="selectPayment('vodafone')">
                            <span class="payment-icon">📱</span>
                            <div>Vodafone Cash</div>
                        </div>
                        <div class="payment-method" onclick="selectPayment('fawry')">
                            <span class="payment-icon">🏪</span>
                            <div>Fawry</div>
                        </div>
                    </div>
                    
                    <input type="hidden" id="paymentMethod" name="paymentMethod" required>
                    
                    <div id="creditCardDetails" style="display: none;">
                        <div class="form-group">
                            <label for="cardNumber">Card Number</label>
                            <input type="text" id="cardNumber" name="cardNumber" class="form-control" placeholder="1234 5678 9012 3456">
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div class="form-group">
                                <label for="expiryDate">Expiry Date</label>
                                <input type="text" id="expiryDate" name="expiryDate" class="form-control" placeholder="MM/YY">
                            </div>
                            
                            <div class="form-group">
                                <label for="cvv">CVV</label>
                                <input type="text" id="cvv" name="cvv" class="form-control" placeholder="123">
                            </div>
                        </div>
                    </div>
                    
                    <div class="security-badge">
                        <span style="font-size: 1.5rem;">🛡️</span>
                        <span>Your payment information is securely encrypted</span>
                    </div>
                </form>
            </div>
            
            <div class="checkout-section">
                <h2 class="section-title">Order Summary</h2>
                <div class="order-summary">
                    {"".join([f'''
                    <div class="order-item">
                        <div>
                            <strong>{item['title']}</strong>
                            <br>
                            <small style="color: rgba(255, 255, 255, 0.7);">By {item['author']}</small>
                        </div>
                        <div style="color: var(--luxury-gold); font-weight: 600;">
                            EGP {item['price']}
                        </div>
                    </div>
                    ''' for item in cart])}
                    
                    <div class="order-total">
                        <div>Total Investment</div>
                        <div style="color: var(--luxury-gold);">EGP {total}</div>
                    </div>
                </div>
                
                <div style="background: rgba(46, 139, 87, 0.1); border-radius: 15px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid rgba(46, 139, 87, 0.3);">
                    <h3 style="color: var(--emerald); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                        <span>🎁</span>
                        <span>Instant Access Guaranteed</span>
                    </h3>
                    <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; line-height: 1.5;">
                        Your premium e-books will be available immediately after payment confirmation. 
                        No waiting, no delays - just instant access to your digital library.
                    </p>
                </div>
                
                <button type="submit" form="checkoutForm" class="btn" style="width: 100%; padding: 1.5rem; font-size: 1.2rem;">
                    <span>Complete Purchase</span>
                    <span>✨</span>
                </button>
                
                <div style="text-align: center; margin-top: 1.5rem;">
                    <a href="/cart" class="btn btn-outline" style="width: 100%;">← Back to Cart</a>
                </div>
            </div>
        </div>
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>MyLibrary</h3>
                    <p>Egypt's premier destination for premium digital literature.</p>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>📞 +20 123 456 7890</p>
                    <p>✉️ premium@mylibrary.com</p>
                    <p>📍 Downtown Cairo, Egypt</p>
                </div>
            </div>
            <div class="copyright">
                <p>© 2024 MyLibrary - Premium Digital Library. Downtown Cairo, Egypt. All Rights Reserved.</p>
            </div>
        </footer>
        
        <script>
            function selectPayment(method) {{
                // Remove selected class from all payment methods
                document.querySelectorAll('.payment-method').forEach(el => {{
                    el.classList.remove('selected');
                }});
                
                // Add selected class to clicked payment method
                event.currentTarget.classList.add('selected');
                
                // Set the payment method value
                document.getElementById('paymentMethod').value = method;
                
                // Show/hide credit card details
                const creditCardDetails = document.getElementById('creditCardDetails');
                if (method === 'credit') {{
                    creditCardDetails.style.display = 'block';
                }} else {{
                    creditCardDetails.style.display = 'none';
                }}
            }}
            
            // Form validation
            document.getElementById('checkoutForm').addEventListener('submit', function(e) {{
                const paymentMethod = document.getElementById('paymentMethod').value;
                if (!paymentMethod) {{
                    e.preventDefault();
                    alert('Please select a payment method');
                    return false;
                }}
            }});
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, cart=cart, total=total, cart_count=len(cart))

# Process Payment
@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Get form data
    full_name = request.form.get('fullName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    payment_method = request.form.get('paymentMethod')
    
    # Process the payment (in a real application, you'd integrate with payment gateways here)
    total = sum(b["price"] * b["quantity"] for b in cart)
    
    # Add books to library
    for book in cart:
        library.append(book)
    
    # Clear cart
    cart.clear()
    
    # Redirect to order confirmation
    return redirect(url_for('order_confirmation', total=total))

# Order Confirmation Page
@app.route('/order_confirmation')
def order_confirmation():
    total = request.args.get('total', 0)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Order Confirmation - MyLibrary</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        {enhanced_styles}
        <style>
            .confirmation-container {{
                max-width: 800px;
                margin: 3rem auto;
                padding: 0 2rem;
                text-align: center;
            }}
            
            .confirmation-card {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 30px;
                padding: 5rem 3rem;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                position: relative;
            }}
            
            .confirmation-card::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 6px;
                background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
            }}
            
            .success-icon {{
                font-size: 8rem;
                margin-bottom: 3rem;
                display: block;
                background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gentleFloat 4s ease-in-out infinite;
            }}
            
            .confirmation-title {{
                font-size: 3.5rem;
                margin-bottom: 2rem;
                background: linear-gradient(135deg, #FFFFFF, var(--luxury-gold));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: 'Playfair Display', serif;
                font-weight: 700;
                text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }}
            
            .confirmation-message {{
                font-size: 1.4rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 3rem;
                line-height: 1.6;
            }}
            
            .order-details {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 20px;
                padding: 2.5rem;
                margin: 3rem 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .detail-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .detail-item:last-child {{
                border-bottom: none;
            }}
            
            .total-amount {{
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--luxury-gold);
                margin: 2rem 0;
                text-shadow: 0 2px 15px rgba(201, 169, 110, 0.5);
            }}
            
            .next-steps {{
                background: rgba(46, 139, 87, 0.1);
                border-radius: 20px;
                padding: 2.5rem;
                margin: 3rem 0;
                border: 1px solid rgba(46, 139, 87, 0.3);
                text-align: left;
            }}
            
            .next-steps h3 {{
                color: var(--emerald);
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                gap: 1rem;
                font-family: 'Playfair Display', serif;
            }}
            
            .next-steps ul {{
                list-style: none;
            }}
            
            .next-steps li {{
                margin-bottom: 1rem;
                color: rgba(255, 255, 255, 0.8);
                display: flex;
                align-items: center;
                gap: 1rem;
            }}
            
            .next-steps li::before {{
                content: "✓";
                color: var(--emerald);
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="luxury-bg"></div>
        <div class="gold-overlay"></div>
        
        <header>
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📚</span>
                    <span>MyLibrary</span>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/all-books">All Collections</a></li>
                        <li><a href="/cart">Cart <span class="cart-count">{len(cart)}</span></a></li>
                        <li><a href="/library">My Library <span class="library-count">{len(library)}</span></a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <div class="confirmation-container">
            <div class="confirmation-card">
                <span class="success-icon">🎉</span>
                <h1 class="confirmation-title">Purchase Complete!</h1>
                <p class="confirmation-message">
                    Thank you for your investment in knowledge. Your premium e-books are now available 
                    in your personal library and ready for immediate access.
                </p>
                
                <div class="order-details">
                    <div class="detail-item">
                        <span>Order Status</span>
                        <span style="color: var(--emerald); font-weight: 600;">Completed</span>
                    </div>
                    <div class="detail-item">
                        <span>Delivery</span>
                        <span style="color: var(--emerald); font-weight: 600;">Instant Access</span>
                    </div>
                    <div class="detail-item">
                        <span>Books Added</span>
                        <span style="color: var(--luxury-gold); font-weight: 600;">{len(library)} Masterpieces</span>
                    </div>
                </div>
                
                <div class="total-amount">
                    Total Investment: EGP {total}
                </div>
                
                <div class="next-steps">
                    <h3>
                        <span>📚</span>
                        <span>What's Next?</span>
                    </h3>
                    <ul>
                        <li>Access your books immediately in "My Library"</li>
                        <li>Download your e-books in multiple formats</li>
                        <li>Start reading on any device - no limits</li>
                        <li>Receive reading recommendations based on your collection</li>
                    </ul>
                </div>
                
                <div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap;">
                    <a href="/library" class="btn">
                        <span>Access My Library</span>
                        <span>📖</span>
                    </a>
                    <a href="/all-books" class="btn btn-outline">
                        <span>Continue Exploring</span>
                        <span>✨</span>
                    </a>
                </div>
            </div>
        </div>
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>MyLibrary</h3>
                    <p>Egypt's premier destination for premium digital literature.</p>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>📞 +20 123 456 7890</p>
                    <p>✉️ premium@mylibrary.com</p>
                    <p>📍 Downtown Cairo, Egypt</p>
                </div>
            </div>
            <div class="copyright">
                <p>© 2024 MyLibrary - Premium Digital Library. Downtown Cairo, Egypt. All Rights Reserved.</p>
            </div>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html, cart_count=len(cart), library_count=len(library))

# My Library Page
@app.route('/library')
def my_library():
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Library - MyLibrary</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        {enhanced_styles}
        <style>
            .library-container {{
                max-width: 1400px;
                margin: 3rem auto;
                padding: 0 2rem;
            }}
            
            .library-header {{
                text-align: center;
                margin-bottom: 4rem;
            }}
            
            .library-title {{
                font-size: 3.5rem;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, #FFFFFF, var(--luxury-gold));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: 'Playfair Display', serif;
                font-weight: 700;
                text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }}
            
            .library-stats {{
                display: flex;
                justify-content: center;
                gap: 3rem;
                margin-bottom: 3rem;
                flex-wrap: wrap;
            }}
            
            .stat-card {{
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 2rem;
                text-align: center;
                min-width: 200px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .stat-number {{
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--luxury-gold);
                margin-bottom: 0.5rem;
            }}
            
            .stat-label {{
                color: rgba(255, 255, 255, 0.8);
                font-size: 1.1rem;
            }}
            
            .empty-library {{
                text-align: center;
                padding: 6rem 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 30px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .empty-library-icon {{
                font-size: 8rem;
                margin-bottom: 3rem;
                display: block;
                background: linear-gradient(135deg, var(--luxury-gold), var(--emerald));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gentleFloat 4s ease-in-out infinite;
            }}
        </style>
    </head>
    <body>
        <div class="luxury-bg"></div>
        <div class="gold-overlay"></div>
        
        <header>
            <div class="header-content">
                <div class="logo">
                    <span class="logo-icon">📚</span>
                    <span>MyLibrary</span>
                </div>
                <nav>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/all-books">All Collections</a></li>
                        <li><a href="/cart">Cart <span class="cart-count">{len(cart)}</span></a></li>
                        <li><a href="/library">My Library <span class="library-count">{len(library)}</span></a></li>
                    </ul>
                </nav>
            </div>
        </header>
        
        <div class="library-container">
            <div class="library-header">
                <h1 class="library-title">My Personal Library</h1>
                <p style="font-size: 1.3rem; color: rgba(255, 255, 255, 0.8); max-width: 600px; margin: 0 auto;">
                    Your curated collection of premium digital masterpieces, available anytime, anywhere.
                </p>
            </div>
            
            <div class="library-stats">
                <div class="stat-card">
                    <div class="stat-number">{len(library)}</div>
                    <div class="stat-label">Total Books</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(set([book['category'] for book in library]))}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{sum([book['pages'] for book in library])}</div>
                    <div class="stat-label">Total Pages</div>
                </div>
            </div>
            
            {"".join([f'''
            <div class="books-grid">
                {"".join([f'''
                <div class="book-card" style="--book-gradient: {book['gradient']}">
                    <span class="book-icon" style="color: {book['color']}">{book['icon']}</span>
                    <div class="book-category">{book['category']}</div>
                    <h3 class="book-title">{book['title']}</h3>
                    <p class="book-author">By {book['author']}</p>
                    <div class="book-details">
                        <span>📄 {book['pages']} pages</span>
                        <span>📝 {book['format']}</span>
                    </div>
                    <div class="book-actions">
                        <button class="btn" style="width: 100%; margin-bottom: 1rem;">
                            <span>📥 Download</span>
                        </button>
                        <button class="btn btn-outline" style="width: 100%;">
                            <span>👁️ Read Online</span>
                        </button>
                    </div>
                </div>
                ''' for book in library])}
            </div>
            ''']) if library else f'''
            <div class="empty-library">
                <span class="empty-library-icon">📚</span>
                <h2 style="font-size: 2.5rem; color: white; margin-bottom: 1.5rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">Your library awaits</h2>
                <p style="font-size: 1.3rem; color: rgba(255, 255, 255, 0.8); margin-bottom: 3rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">
                    Start building your premium collection by exploring our masterpieces
                </p>
                <a href="/all-books" class="btn">Explore Masterpieces</a>
            </div>
            '''}
        </div>
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>MyLibrary</h3>
                    <p>Egypt's premier destination for premium digital literature.</p>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>📞 +20 123 456 7890</p>
                    <p>✉️ premium@mylibrary.com</p>
                    <p>📍 Downtown Cairo, Egypt</p>
                </div>
            </div>
            <div class="copyright">
                <p>© 2024 MyLibrary - Premium Digital Library. Downtown Cairo, Egypt. All Rights Reserved.</p>
            </div>
        </footer>
    </body>
    </html>
    '''
    return render_template_string(html, cart_count=len(cart), library_count=len(library))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)