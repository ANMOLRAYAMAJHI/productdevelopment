"""
Seed script — populates Gallery, Events, Feedback, Services, and Blog
with realistic sample data. Safe to re-run: skips tables that already have rows.
"""
from datetime import datetime
from app import app
from models import db, GalleryItem, EventTimeline, Feedback, ServiceItem, BlogPost


GALLERY = [
    {
        "title": "Product Launch Night",
        "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=900&q=80",
        "caption": "Unveiling our newest release to a packed room of early adopters.",
    },
    {
        "title": "Team Offsite — Coastal Retreat",
        "image_url": "https://images.unsplash.com/photo-1511578314322-379afb476865?w=900&q=80",
        "caption": "Strategy sessions and team bonding by the coast.",
    },
    {
        "title": "Annual Conference Keynote",
        "image_url": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=900&q=80",
        "caption": "Sharing our product roadmap on the main stage to 1,200 attendees.",
    },
    {
        "title": "Office Culture",
        "image_url": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=900&q=80",
        "caption": "A glimpse into our open, collaborative day-to-day workspace.",
    },
    {
        "title": "Client Workshop",
        "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=900&q=80",
        "caption": "Collaborating with enterprise partners on next-generation workflows.",
    },
    {
        "title": "Behind the Scenes",
        "image_url": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=900&q=80",
        "caption": "Our crew prepping for the big event — every detail counts.",
    },
    {
        "title": "Hackathon 2024",
        "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=900&q=80",
        "caption": "48 hours of building, debugging, and creative problem-solving.",
    },
    {
        "title": "Community Meetup",
        "image_url": "https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=900&q=80",
        "caption": "Connecting with our developer community over ideas and demos.",
    },
    {
        "title": "Award Ceremony",
        "image_url": "https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=900&q=80",
        "caption": "Proud to receive the Best SaaS Innovation Award at TechForward 2024.",
    },
]

EVENTS = [
    {
        "title": "Company Founded",
        "description": "We officially launched with a founding team of five engineers and one bold mission — to make customer support genuinely intelligent.",
        "event_date": datetime(2022, 3, 10),
    },
    {
        "title": "Seed Round Closed",
        "description": "Raised $1.2M in seed funding from angel investors to build the first version of the AI helpdesk platform.",
        "event_date": datetime(2022, 8, 22),
    },
    {
        "title": "Beta Launch",
        "description": "Released a private beta to 50 early-access customers and gathered the feedback that shaped our product direction.",
        "event_date": datetime(2023, 1, 15),
    },
    {
        "title": "First Product Release (v1.0)",
        "description": "Shipped the first stable public release with ticket management, sentiment analysis, and admin dashboard fully operational.",
        "event_date": datetime(2023, 5, 3),
    },
    {
        "title": "1,000 Users Milestone",
        "description": "Crossed a thousand active users within six months of launch — a major validation of our product-market fit.",
        "event_date": datetime(2023, 10, 18),
    },
    {
        "title": "Series A Funding — $4.5M",
        "description": "Secured Series A funding to expand the engineering team, accelerate AI features, and enter new markets.",
        "event_date": datetime(2024, 2, 7),
    },
    {
        "title": "Virtual Assistant Feature Launched",
        "description": "Rolled out the AI-powered virtual assistant widget — enabling customers to get instant guidance without opening a ticket.",
        "event_date": datetime(2024, 4, 20),
    },
    {
        "title": "New Headquarters Opened",
        "description": "Moved into a purpose-built 8,000 sq ft office designed for hybrid teams, with focus pods, open collaboration zones, and a rooftop deck.",
        "event_date": datetime(2024, 7, 1),
    },
    {
        "title": "10,000 Users Milestone",
        "description": "Reached ten thousand active users across 34 countries — solidifying our position as a global helpdesk platform.",
        "event_date": datetime(2024, 11, 11),
    },
    {
        "title": "Enterprise Tier Launched",
        "description": "Released enterprise-grade features including SLA management, multi-team routing, and SSO integration.",
        "event_date": datetime(2025, 3, 5),
    },
    {
        "title": "Best SaaS Innovation Award",
        "description": "Awarded Best SaaS Innovation at TechForward 2025 — recognised for our sentiment-driven ticket prioritisation engine.",
        "event_date": datetime(2025, 6, 14),
    },
]

FEEDBACK = [
    {
        "name": "Sarah Mitchell",
        "role": "Head of Customer Success, NovaTech",
        "message": "This platform transformed the way our support team operates. Ticket routing is now instant and accurate, and our response times dropped by 40% in the first month alone.",
        "rating": 5,
    },
    {
        "name": "James Okafor",
        "role": "CTO, Streamline Labs",
        "message": "The sentiment analysis is genuinely impressive. We can now spot frustrated customers before they escalate and act proactively. The admin dashboard is clean and gives us exactly the insight we need.",
        "rating": 5,
    },
    {
        "name": "Priya Sharma",
        "role": "Product Manager, CloudBridge",
        "message": "Setup was straightforward and the interface is intuitive for both customers and admins. The virtual assistant alone saves our team hours every week.",
        "rating": 5,
    },
    {
        "name": "Lucas Ferreira",
        "role": "Operations Lead, QuickCart",
        "message": "We evaluated five helpdesk tools and this was the only one that offered AI prioritization out of the box without requiring a data science team to configure it. Solid value.",
        "rating": 4,
    },
    {
        "name": "Emily Zhao",
        "role": "Support Manager, Finbloom",
        "message": "The analytics dashboard helped us identify our peak ticket hours and restructure shift scheduling accordingly. A simple but impactful insight we didn't have before.",
        "rating": 5,
    },
    {
        "name": "Daniel Kowalski",
        "role": "Founder, DevStack Agency",
        "message": "As a small agency, we needed a system that didn't require a dedicated IT person to manage. This fits perfectly — we were live in under an hour.",
        "rating": 4,
    },
    {
        "name": "Amara Nwosu",
        "role": "Customer Experience Director, PulseRetail",
        "message": "Our NPS score improved by 18 points in Q3 after switching. The transparent ticket tracking builds real trust with customers and reduces the 'where is my request?' follow-ups.",
        "rating": 5,
    },
    {
        "name": "Tom Bergstein",
        "role": "IT Manager, MedCore Solutions",
        "message": "Security was our main concern given our industry. The CSRF protection, secure headers, and audit-friendly logging made compliance approval much easier. Very pleased.",
        "rating": 5,
    },
    {
        "name": "Ayesha Malik",
        "role": "Startup Founder, SprintHR",
        "message": "The blog and services sections help us keep clients informed without juggling a separate CMS. Everything in one platform is a huge time saver for a lean team.",
        "rating": 4,
    },
    {
        "name": "Ravi Menon",
        "role": "VP Engineering, DataPilot",
        "message": "Integration took a weekend and the documentation is clear. The event timeline feature is a nice touch for showcasing company milestones to new visitors.",
        "rating": 5,
    },
]

SERVICES = [
    {
        "title": "AI Ticket Management",
        "description": "Automatically classify, prioritize, and route incoming support tickets using sentiment analysis. Urgent issues surface instantly so your team never misses a critical request.",
        "icon": "🎫",
    },
    {
        "title": "Virtual Assistant",
        "description": "Deploy a conversational AI widget that guides customers through ticket submission, status checks, and common queries — reducing first-response load by up to 60%.",
        "icon": "🤖",
    },
    {
        "title": "Analytics Dashboard",
        "description": "Real-time visibility into ticket volumes, sentiment trends, resolution rates, and team performance — all in a single, clean admin view.",
        "icon": "📊",
    },
    {
        "title": "Service Portfolio CMS",
        "description": "Publish and manage your software solutions, product offerings, and service descriptions directly from the admin panel — no developer needed.",
        "icon": "🧩",
    },
    {
        "title": "Events & Milestones Timeline",
        "description": "Showcase your company journey, product launches, and key achievements with an interactive timeline that builds credibility with prospects and customers.",
        "icon": "📅",
    },
    {
        "title": "Photo Gallery & Blog",
        "description": "Share team photos, event highlights, and thought leadership articles. Keep your audience engaged with fresh visual and written content managed from one place.",
        "icon": "📸",
    },
    {
        "title": "Customer Feedback Hub",
        "description": "Collect, curate, and display customer reviews and star ratings. Highlight positive testimonials to build trust and convert new visitors.",
        "icon": "⭐",
    },
    {
        "title": "Contact & Inquiry Management",
        "description": "Centralise all inbound contact form submissions with read/unread tracking, ensuring no customer inquiry slips through the cracks.",
        "icon": "📬",
    },
    {
        "title": "Enterprise Security Suite",
        "description": "OWASP-aligned protection including CSRF tokens, rate limiting, XSS prevention, secure session handling, and HTTP security headers — enabled by default.",
        "icon": "🔐",
    },
]

BLOG_POSTS = [
    {
        "title": "How AI Sentiment Analysis Cuts Support Response Time in Half",
        "excerpt": "Traditional helpdesks treat every ticket the same. AI-driven sentiment scoring changes that — here's how our engine identifies urgency the moment a ticket arrives.",
        "body": "Traditional helpdesks treat every ticket the same. AI-driven sentiment scoring changes that — here's how our engine identifies urgency the moment a ticket arrives. We analysed 50,000 tickets and the results speak for themselves.",
        "image_url": "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=800&q=80",
    },
    {
        "title": "5 Signs Your Support Team Has Outgrown Its Current Helpdesk",
        "excerpt": "When tickets start falling through the cracks, SLAs get missed, and your team is manually triaging every request — it's time for an upgrade.",
        "body": "When tickets start falling through the cracks, SLAs get missed, and your team is manually triaging every request — it's time for an upgrade. Here are five warning signs to watch for.",
        "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80",
    },
    {
        "title": "Building a Knowledge Base That Actually Reduces Ticket Volume",
        "excerpt": "A well-structured knowledge base can deflect up to 30% of incoming tickets. We break down exactly how to structure yours for maximum self-service adoption.",
        "body": "A well-structured knowledge base can deflect up to 30% of incoming tickets. We break down exactly how to structure yours for maximum self-service adoption.",
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    },
    {
        "title": "The Real Cost of Slow Customer Support (And How to Fix It)",
        "excerpt": "Research shows 73% of customers switch brands after a poor support experience. We dig into the numbers and share the fixes that actually move the needle.",
        "body": "Research shows 73% of customers switch brands after a poor support experience. We dig into the numbers and share the fixes that actually move the needle.",
        "image_url": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80",
    },
    {
        "title": "OWASP Top 10 for SaaS Products: A Practical Checklist",
        "excerpt": "Security is not optional. We walk through the OWASP Top 10 vulnerabilities and show exactly how each one is addressed in our platform architecture.",
        "body": "Security is not optional. We walk through the OWASP Top 10 vulnerabilities and show exactly how each one is addressed in our platform architecture.",
        "image_url": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&q=80",
    },
    {
        "title": "What Great Customer Feedback Looks Like (And How to Gather More of It)",
        "excerpt": "A 5-star review is worth more than a marketing campaign. Here's our framework for turning satisfied customers into vocal advocates.",
        "body": "A 5-star review is worth more than a marketing campaign. Here's our framework for turning satisfied customers into vocal advocates.",
        "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80",
    },
]


def next_id(model):
    """Return the next safe integer ID for any DB (Oracle, SQLite, etc.)."""
    from sqlalchemy import func
    max_val = db.session.query(func.max(model.id)).scalar()
    return (max_val or 0) + 1


def seed():
    with app.app_context():
        seeded = []

        if GalleryItem.query.count() == 0:
            start = next_id(GalleryItem)
            for i, g in enumerate(GALLERY):
                item = GalleryItem(**g, active=True)
                item.id = start + i
                db.session.add(item)
            db.session.flush()
            seeded.append(f"{len(GALLERY)} gallery items")

        if EventTimeline.query.count() == 0:
            start = next_id(EventTimeline)
            for i, e in enumerate(EVENTS):
                item = EventTimeline(**e, position=i, active=True)
                item.id = start + i
                db.session.add(item)
            db.session.flush()
            seeded.append(f"{len(EVENTS)} events")

        if Feedback.query.count() == 0:
            start = next_id(Feedback)
            for i, f in enumerate(FEEDBACK):
                item = Feedback(**f, active=True)
                item.id = start + i
                db.session.add(item)
            db.session.flush()
            seeded.append(f"{len(FEEDBACK)} feedback entries")

        if ServiceItem.query.count() == 0:
            start = next_id(ServiceItem)
            for i, s in enumerate(SERVICES):
                item = ServiceItem(**s, active=True)
                item.id = start + i
                db.session.add(item)
            db.session.flush()
            seeded.append(f"{len(SERVICES)} services")

        if BlogPost.query.count() == 0:
            start = next_id(BlogPost)
            for i, b in enumerate(BLOG_POSTS):
                item = BlogPost(**b, active=True)
                item.id = start + i
                db.session.add(item)
            db.session.flush()
            seeded.append(f"{len(BLOG_POSTS)} blog posts")

        if seeded:
            db.session.commit()
            print("Seeded: " + ", ".join(seeded))
        else:
            print("Nothing to seed — all tables already have data.")


if __name__ == "__main__":
    seed()
