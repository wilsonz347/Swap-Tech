# Swap Tech

## Description
Swap Tech is a platform that promotes eco-friendly tech consumption by facilitating the refurbishment and recycling of electronic devices. The platform supports two user types: refurbishers who can purchase, refurbish, and sell devices, and recyclers who can buy verified refurbished devices.

## Tech Stack
### Backend
- Django
- Flask 
- PyTorch
- Transformers
- Pillow

### Frontend
- Django Templates
- HTML
- CSS
- JavaScript

## Installation

1. Clone the repository
```bash
git clone https://github.com/wilsonz347/Swap-Tech.git
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

4. Run Django migrations
```bash
python manage.py migrate
```

5. Start servers
```bash
cd backend/general_backend
python manage.py runserver
```
```bash
Navigate to root directory
cd backend/ai_integrate
python chatbot.py
```


## Features

Dual user roles (Refurbisher/Recycler)
Device marketplace
User authentication system
AI-powered chatbot
Profile management
Notification system

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Challenges We Faced

### Technical Challenges
1. Setting up dual authentication flows for refurbishers and recyclers

### Implementation Challenges
1. Connecting Flask-based chatbot with Django main application

2. Implementing live notifications for marketplace updates

### Development Process Challenges
1. Balancing feature implementation within hackathon timeframe

### Future Improvements
- Implement location/direct swap to find sustainable resources near the user's area.
- Live-tracking user sustainability based on off their contributions
