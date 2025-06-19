# Prospec - AI-Powered Lead Generation Platform

A modern Vue.js application for intelligent prospect discovery and engagement management. Prospec leverages AI to help sales teams find, qualify, and engage with potential customers through personalized outreach campaigns.

## 🚀 Features

### Lead Discovery & Management
- **AI-Powered Search**: Natural language queries to find ideal prospects
- **Advanced Filtering**: Filter by industry, company size, location, job titles, and keywords
- **Lead Organization**: Categorize leads into New, Saved, and Archived tabs
- **Comprehensive Data**: Access to contact information, LinkedIn profiles, and company details

### Engagement Hub
- **Icebreaker Management**: Create and track personalized outreach messages
- **Follow-up Scheduling**: Automated reminders for prospect engagement
- **Status Tracking**: Monitor engagement progress from initial contact to conversion
- **Lead Workspace**: Dedicated interface for managing individual prospect interactions

### User Experience
- **Internationalization**: Full support for English and Traditional Chinese (繁體中文)
- **Responsive Design**: Optimized for desktop and mobile devices
- **Theme Support**: Light and dark mode options
- **Real-time Updates**: Automatic version checking and update notifications

## 🛠 Tech Stack

- **Frontend**: Vue 3 + TypeScript + Vite
- **UI Framework**: Bootstrap 5 with Bootstrap Icons
- **State Management**: Pinia
- **Authentication**: Supabase Auth
- **Database**: Supabase
- **Routing**: Vue Router with authentication guards
- **Build Tool**: Vite with custom build optimization

## 📋 Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Supabase account and project

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd lead-gen
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Setup
Create a `.env.local` file in the root directory:
```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 4. Development Server
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 5. Build for Production
```bash
npm run build
```

## 📁 Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── AppNavigationSidebar.vue
│   └── FilterPanelView.vue
├── views/              # Page-level components
│   ├── LeadGenFormView.vue      # Main prospect search interface
│   ├── EngagementCenterView.vue # Lead engagement management
│   ├── LoginView.vue            # Authentication
│   └── SignUpView.vue
├── stores/             # Pinia state management
│   ├── authStore.ts            # Authentication state
│   └── languageStore.ts        # Internationalization
├── services/           # External service integrations
│   └── supabaseClient.ts       # Supabase configuration
├── types/              # TypeScript type definitions
│   ├── language.ts             # i18n types and translations
│   ├── forms.ts               # Form-related types
│   └── tabs.ts                # Tab management types
├── router/             # Vue Router configuration
└── assets/             # Static assets
```

## 🔐 Authentication

The application uses Supabase Authentication with:
- Email/password authentication
- Session management with automatic refresh
- Route guards for protected pages
- Automatic redirects based on authentication state

## 🌍 Internationalization

Supported languages:
- English (en)
- Traditional Chinese (zh)

Language switching is available through the navigation sidebar settings.

## 🎨 Theming

The application supports:
- Light mode (default)
- Dark mode
- System preference detection

Theme preferences are persisted across sessions.

## 📱 Key Pages

### Prospect Search (`/`)
Main interface for discovering and managing leads with:
- Natural language search capabilities
- Advanced filtering options
- Tabbed lead organization
- Bulk actions for lead management

### Engagement Hub (`/engagement-hub`)
Dedicated workspace for managing prospect interactions:
- Lead queue with status filtering
- Icebreaker message composition
- Follow-up scheduling
- Engagement tracking

## 🔧 Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run generate-build-info` - Generate build metadata

### Code Style
- TypeScript for type safety
- Vue 3 Composition API with `<script setup>`
- Bootstrap utility classes for styling
- ESLint and Prettier for code formatting

## 🚀 Deployment

The application is optimized for deployment on:
- Vercel
- Netlify
- Any static hosting service

Ensure environment variables are configured in your deployment platform.

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support contact information here]
