const translations = {
    en: {
        nav_home: "Home",
        nav_apps: "Apps",
        nav_download: "Download",
        nav_contact: "Contact",
        hero_title: "Innovative Mobile Applications",
        hero_subtitle: "Discover cutting-edge apps powered by AI technology to enhance social life experience",
        hero_cta: "Explore Our Apps",
        apps_title: "Our Applications",
        app_qr_title: "Digital QR Card",
        app_qr_desc: "Manage and share your digital business cards effortlessly. Create professional cards with QR codes and share them instantly.",
        app_qr_feat1: "Digital Business Cards",
        app_qr_feat2: "QR Code Sharing",
        app_qr_feat3: "Easy Share",
        app_qr_btn: "Visit Website →",
        app_ww_title: "Wise Weather",
        app_ww_desc: "Community-based weather app providing real-time weather updates and forecasts powered by collective intelligence.",
        app_ww_feat1: "Community Weather Reports",
        app_ww_feat2: "Real-time Forecasts",
        app_ww_feat3: "Get Rain, Wind & Snow Alerts",
        app_ww_btn: "Visit Website →",
        download_title: "Download Our Apps",
        platform_ios: "App Store",
        platform_ios_desc: "Available on iOS devices",
        platform_android: "Google Play",
        platform_android_desc: "Available on Android devices",
        platform_web: "Web App",
        platform_web_desc: "Access from any browser",
        custom_title: "Custom Development",
        custom_card_title: "Bring Your Idea to Life",
        custom_card_desc: "Looking to build your mobile application, website, or platform? We offer premium development services tailored to your needs.",
        custom_feat1: "Mobile Apps",
        custom_feat2: "Web Platforms",
        custom_feat3: "AI Integration",
        custom_btn: "Request a Quote",
        contact_title: "Get in Touch",
        form_name: "Name",
        form_email: "Email",
        form_message: "Message",
        form_topic_default: "Select a topic",
        form_topic_digital: "Digital QR Card App",
        form_topic_weather: "Wise Weather App",
        form_topic_support: "Technical Support",
        form_topic_feedback: "Feedback",
        form_topic_partnership: "Partnership",
        form_topic_quote: "Request a Quote",
        form_topic_other: "Other",
        form_btn: "Send",
        footer_copy: "&copy; 2024 Global Workflow. All rights reserved.",
        footer_location: "Based in Geneva (Switzerland)"
    },
    fr: {
        nav_home: "Accueil",
        nav_apps: "Apps",
        nav_download: "Téléchargement",
        nav_contact: "Contact",
        hero_title: "Applications Mobiles Innovantes",
        hero_subtitle: "Découvrez des applications de pointe propulsées par l'IA pour enrichir votre vie sociale",
        hero_cta: "Explorer nos Apps",
        apps_title: "Nos Applications",
        app_qr_title: "Digital QR Card",
        app_qr_desc: "Gérez et partagez vos cartes de visite numériques sans effort. Créez des cartes professionnelles avec QR codes et partagez-les instantanément.",
        app_qr_feat1: "Cartes de Visite Numériques",
        app_qr_feat2: "Partage par QR Code",
        app_qr_feat3: "Partage Facile",
        app_qr_btn: "Visiter le Site →",
        app_ww_title: "Wise Weather",
        app_ww_desc: "Application météo communautaire fournissant des mises à jour et prévisions en temps réel propulsées par l'intelligence collective.",
        app_ww_feat1: "Reports Météo Communautaires",
        app_ww_feat2: "Prévisions en Temps Réel",
        app_ww_feat3: "Alertes Pluie, Vent & Neige",
        app_ww_btn: "Visiter le Site →",
        download_title: "Télécharger Nos Apps",
        platform_ios: "App Store",
        platform_ios_desc: "Disponible sur iOS",
        platform_android: "Google Play",
        platform_android_desc: "Disponible sur Android",
        platform_web: "Web App",
        platform_web_desc: "Accès depuis tout navigateur",
        custom_title: "Développement Sur Mesure",
        custom_card_title: "Donnez Vie à Vos Idées",
        custom_card_desc: "Vous souhaitez créer votre application mobile, site web ou plateforme ? Nous offrons des services de développement premium adaptés à vos besoins.",
        custom_feat1: "Applications Mobiles",
        custom_feat2: "Plateformes Web",
        custom_feat3: "Intégration IA",
        custom_btn: "Demander un Devis",
        contact_title: "Contactez-nous",
        form_name: "Nom",
        form_email: "Email",
        form_message: "Message",
        form_topic_default: "Sélectionnez un sujet",
        form_topic_digital: "App Digital QR Card",
        form_topic_weather: "App Wise Weather",
        form_topic_support: "Support Technique",
        form_topic_feedback: "Retours & Suggestions",
        form_topic_partnership: "Partenariat",
        form_topic_quote: "Demande de Devis",
        form_topic_other: "Autre",
        form_btn: "Envoyer",
        footer_copy: "&copy; 2024 Global Workflow. Tous droits réservés.",
        footer_location: "Basé à Genève (Suisse)"
    }
};

function setLanguage(lang) {
    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang][key]) {
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translations[lang][key];
            } else {
                element.innerHTML = translations[lang][key];
            }
        }
    });

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    localStorage.setItem('preferredLanguage', lang);
}

document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLanguage') || 'en';
    setLanguage(savedLang);

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            setLanguage(btn.dataset.lang);
        });
    });
});
