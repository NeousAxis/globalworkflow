from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
from pathlib import Path
import openai
import requests
from datetime import datetime
import json
import uuid
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
app = FastAPI(
    title="Zeus AI Agent",
    description="Agent IA pour la création automatisée de contenu",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration APIs
openai.api_key = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
LOCAL_STORAGE_PATH = os.getenv('LOCAL_STORAGE_PATH', './zeus-content')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

# Modèles de données
class VideoRequest(BaseModel):
    topic: str
    duration: int = 60
    style: str = "educational"
    target_audience: str = "professionals"

class SocialPostRequest(BaseModel):
    platform: str
    topic: str
    tone: str = "professional"
    include_hashtags: bool = True

class VisualRequest(BaseModel):
    type: str
    style: str
    description: str
    dimensions: str = "1080x1080"

class PodcastRequest(BaseModel):
    topic: str
    duration: int = 30
    voice_style: str = "conversational"
    include_intro: bool = True

class ReportRequest(BaseModel):
    topic: str
    data_sources: List[str] = []
    format: str = "pdf"
    include_charts: bool = True

class WeeklyContentRequest(BaseModel):
    theme: str
    platforms: List[str]
    content_types: List[str]
    schedule_date: str

class ZeusResponse(BaseModel):
    status: str
    service: str
    content: dict
    metadata: dict
    optimization_suggestions: List[str]

# Gestionnaire de stockage local
class LocalStorageManager:
    def __init__(self):
        self.base_path = Path(LOCAL_STORAGE_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Créer les dossiers
        for folder in ['videos', 'images', 'podcasts', 'reports', 'social']:
            (self.base_path / folder).mkdir(exist_ok=True)
    
    def save_file(self, content: bytes, filename: str, content_type: str) -> str:
        """Sauvegarde un fichier localement et retourne l'URL"""
        folder_map = {
            'video': 'videos',
            'image': 'images', 
            'audio': 'podcasts',
            'pdf': 'reports',
            'social': 'social'
        }
        
        folder = folder_map.get(content_type, 'misc')
        file_path = self.base_path / folder / filename
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return f"{BASE_URL}/files/{folder}/{filename}"
    
    def save_text(self, content: str, filename: str, content_type: str) -> str:
        """Sauvegarde du texte localement"""
        return self.save_file(content.encode('utf-8'), filename, content_type)
    
    def get_file_path(self, filename: str, content_type: str) -> Path:
        folder_map = {
            'video': 'videos',
            'image': 'images',
            'audio': 'podcasts', 
            'pdf': 'reports',
            'social': 'social'
        }
        folder = folder_map.get(content_type, 'misc')
        return self.base_path / folder / filename

# Initialiser le gestionnaire de stockage
storage = LocalStorageManager()

# Classes de services
class ContentGenerator:
    @staticmethod
    def generate_script(topic: str, duration: int, style: str) -> str:
        """Génère un script avec OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Tu es un expert en création de contenu {style}. Crée un script engageant de {duration} secondes sur le sujet: {topic}"},
                    {"role": "user", "content": f"Crée un script détaillé pour une vidéo de {duration} secondes sur '{topic}' dans un style {style}. Inclus les indications de mise en scène."}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur lors de la génération du script: {str(e)}"
    
    @staticmethod
    def generate_social_post(platform: str, topic: str, tone: str, include_hashtags: bool) -> str:
        """Génère un post social avec OpenAI"""
        try:
            hashtag_instruction = "Inclus des hashtags pertinents." if include_hashtags else "N'inclus pas de hashtags."
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Tu es un expert en marketing digital spécialisé dans {platform}. Ton ton est {tone}."},
                    {"role": "user", "content": f"Crée un post {platform} sur '{topic}' avec un ton {tone}. {hashtag_instruction} Respecte les bonnes pratiques de {platform}."}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur lors de la génération du post: {str(e)}"

class MediaProcessor:
    @staticmethod
    def generate_audio(text: str, voice_style: str = "conversational") -> str:
        """Génère de l'audio avec ElevenLabs"""
        try:
            # Voix par défaut ElevenLabs (vous pouvez changer l'ID)
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                # Sauvegarder l'audio
                filename = f"audio_{uuid.uuid4().hex[:8]}.mp3"
                audio_url = storage.save_file(response.content, filename, 'audio')
                return audio_url
            else:
                return f"Erreur ElevenLabs: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Erreur lors de la génération audio: {str(e)}"

class ReportGenerator:
    @staticmethod
    def generate_report(topic: str, data_sources: List[str], format: str) -> str:
        """Génère un rapport avec OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un analyste expert en création de rapports professionnels."},
                    {"role": "user", "content": f"Crée un rapport détaillé sur '{topic}'. Sources de données: {', '.join(data_sources) if data_sources else 'Analyse générale'}. Format: {format}. Inclus une introduction, analyse, conclusions et recommandations."}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            # Sauvegarder le rapport
            filename = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            report_url = storage.save_text(response.choices[0].message.content, filename, 'pdf')
            return report_url
            
        except Exception as e:
            return f"Erreur lors de la génération du rapport: {str(e)}"

# Endpoints API
@app.get("/")
async def root():
    return {
        "message": "Zeus AI Agent - Prêt à automatiser votre création de contenu",
        "version": "1.0.0",
        "services": [
            "Création vidéo",
            "Contenu social", 
            "Identité visuelle",
            "Production podcast",
            "Génération rapports",
            "Contenu hebdomadaire"
        ]
    }

@app.post("/api/video/create", response_model=ZeusResponse)
async def create_video(request: VideoRequest):
    """Crée une vidéo automatisée"""
    try:
        # Générer le script
        script = ContentGenerator.generate_script(
            request.topic, 
            request.duration, 
            request.style
        )
        
        # Générer l'audio du script
        audio_url = MediaProcessor.generate_audio(script)
        
        # Sauvegarder le script
        script_filename = f"script_{uuid.uuid4().hex[:8]}.txt"
        script_url = storage.save_text(script, script_filename, 'video')
        
        return ZeusResponse(
            status="success",
            service="video_creation",
            content={
                "script": script,
                "script_url": script_url,
                "audio_url": audio_url,
                "storyboard": ["Scène d'introduction", "Développement du sujet", "Conclusion"]
            },
            metadata={
                "duration": request.duration,
                "style": request.style,
                "created_at": datetime.now().isoformat(),
                "topic": request.topic
            },
            optimization_suggestions=[
                "Ajouter des sous-titres pour l'accessibilité",
                "Optimiser pour le mobile",
                "Ajouter des visuels engageants"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/social/generate", response_model=ZeusResponse)
async def generate_social_content(request: SocialPostRequest):
    """Génère du contenu social automatisé"""
    try:
        post_content = ContentGenerator.generate_social_post(
            request.platform,
            request.topic,
            request.tone,
            request.include_hashtags
        )
        
        # Sauvegarder le post
        filename = f"{request.platform}_post_{uuid.uuid4().hex[:8]}.txt"
        post_url = storage.save_text(post_content, filename, 'social')
        
        return ZeusResponse(
            status="success",
            service="social_content",
            content={
                "post": post_content,
                "post_url": post_url,
                "platform": request.platform,
                "character_count": len(post_content)
            },
            metadata={
                "platform": request.platform,
                "tone": request.tone,
                "created_at": datetime.now().isoformat(),
                "topic": request.topic
            },
            optimization_suggestions=[
                f"Optimal pour {request.platform}",
                "Ajouter des visuels si possible",
                "Programmer la publication aux heures de pointe"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/podcast/create", response_model=ZeusResponse)
async def create_podcast(request: PodcastRequest):
    """Crée un podcast automatisé"""
    try:
        # Générer le script du podcast
        script = ContentGenerator.generate_script(
            request.topic,
            request.duration * 60,  # Convertir en secondes
            "podcast conversationnel"
        )
        
        # Générer l'audio
        audio_url = MediaProcessor.generate_audio(script, request.voice_style)
        
        # Sauvegarder le script
        script_filename = f"podcast_script_{uuid.uuid4().hex[:8]}.txt"
        script_url = storage.save_text(script, script_filename, 'audio')
        
        return ZeusResponse(
            status="success",
            service="podcast_production",
            content={
                "script": script,
                "script_url": script_url,
                "audio_url": audio_url,
                "duration_minutes": request.duration
            },
            metadata={
                "topic": request.topic,
                "duration": request.duration,
                "voice_style": request.voice_style,
                "created_at": datetime.now().isoformat()
            },
            optimization_suggestions=[
                "Ajouter une intro musicale",
                "Créer des chapitres pour la navigation",
                "Optimiser le niveau audio"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/generate", response_model=ZeusResponse)
async def generate_report(request: ReportRequest):
    """Génère un rapport intelligent"""
    try:
        report_url = ReportGenerator.generate_report(
            request.topic,
            request.data_sources,
            request.format
        )
        
        return ZeusResponse(
            status="success",
            service="report_generation",
            content={
                "report_url": report_url,
                "format": request.format,
                "sections": ["Introduction", "Analyse", "Conclusions", "Recommandations"]
            },
            metadata={
                "topic": request.topic,
                "format": request.format,
                "data_sources": request.data_sources,
                "created_at": datetime.now().isoformat()
            },
            optimization_suggestions=[
                "Ajouter des graphiques pour visualiser les données",
                "Inclure un résumé exécutif",
                "Vérifier les sources et références"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ajouter après la classe ReportGenerator (ligne 230)
class VisualGenerator:
    @staticmethod
    def generate_image_prompt(visual_type: str, style: str, description: str) -> str:
        """Génère un prompt optimisé pour DALL-E"""
        prompts = {
            "portrait": f"Professional AI-generated portrait, {style} style, {description}, high quality, detailed, studio lighting",
            "logo": f"Modern logo design, {style} aesthetic, {description}, clean, vector-style, professional branding",
            "banner": f"Social media banner, {style} design, {description}, engaging, high-resolution, marketing-ready",
            "quote": f"Inspirational quote visual, {style} typography, {description}, elegant design, social media ready",
            "branding": f"Brand identity visual, {style} concept, {description}, cohesive design, professional quality"
        }
        return prompts.get(visual_type, f"{style} style visual: {description}")
    
    @staticmethod
    def generate_visual(visual_type: str, style: str, description: str, dimensions: str) -> dict:
        """Génère une image avec DALL-E 3"""
        try:
            prompt = VisualGenerator.generate_image_prompt(visual_type, style, description)
            
            # Convertir les dimensions pour DALL-E
            size_map = {
                "1080x1080": "1024x1024",
                "1920x1080": "1792x1024", 
                "1080x1920": "1024x1792"
            }
            dalle_size = size_map.get(dimensions, "1024x1024")
            
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size=dalle_size,
                quality="hd",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Télécharger et sauvegarder l'image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                filename = f"{visual_type}_{uuid.uuid4().hex[:8]}.png"
                local_url = storage.save_file(image_response.content, filename, "image")
                
                return {
                    "success": True,
                    "image_url": local_url,
                    "original_url": image_url,
                    "prompt_used": prompt,
                    "filename": filename
                }
            else:
                return {"success": False, "error": "Failed to download image"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

# Remplacer l'endpoint /api/visual/create (lignes 402-424)
@app.post("/api/visual/create", response_model=ZeusResponse)
async def create_visual_identity(request: VisualRequest):
    """Crée une identité visuelle avec DALL-E 3"""
    try:
        # Générer l'image
        result = VisualGenerator.generate_visual(
            request.type, 
            request.style, 
            request.description, 
            request.dimensions
        )
        
        if result["success"]:
            return ZeusResponse(
                status="success",
                service="visual_identity",
                content={
                    "type": request.type,
                    "style": request.style,
                    "description": request.description,
                    "image_url": result["image_url"],
                    "filename": result["filename"],
                    "prompt_used": result["prompt_used"],
                    "dimensions": request.dimensions
                },
                metadata={
                    "type": request.type,
                    "style": request.style,
                    "created_at": datetime.now().isoformat(),
                    "model_used": "dall-e-3",
                    "dimensions": request.dimensions
                },
                optimization_suggestions=[
                    "Testez différents styles pour optimiser l'impact visuel",
                    "Considérez des variations de couleurs pour différents usages",
                    "Adaptez les dimensions selon les plateformes cibles"
                ]
            )
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération visuelle: {str(e)}")

@app.post("/api/weekly/generate", response_model=ZeusResponse)
async def generate_weekly_content(request: WeeklyContentRequest):
    """Génère du contenu hebdomadaire automatisé"""
    try:
        weekly_content = []
        
        for platform in request.platforms:
            for content_type in request.content_types:
                if content_type == "posts":
                    post = ContentGenerator.generate_social_post(
                        platform,
                        f"{request.theme} - Semaine du {request.schedule_date}",
                        "professionnel",
                        True
                    )
                    weekly_content.append({
                        "platform": platform,
                        "type": "post",
                        "content": post
                    })
        
        # Sauvegarder le planning
        planning_filename = f"planning_hebdo_{request.schedule_date.replace('-', '')}.json"
        planning_url = storage.save_text(
            json.dumps(weekly_content, indent=2, ensure_ascii=False),
            planning_filename,
            'social'
        )
        
        return ZeusResponse(
            status="success",
            service="weekly_content",
            content={
                "planning_url": planning_url,
                "content_items": len(weekly_content),
                "preview": weekly_content[:2]  # Aperçu des 2 premiers éléments
            },
            metadata={
                "theme": request.theme,
                "platforms": request.platforms,
                "schedule_date": request.schedule_date,
                "created_at": datetime.now().isoformat()
            },
            optimization_suggestions=[
                "Programmer les publications automatiquement",
                "Adapter le contenu selon les heures de pointe",
                "Ajouter des visuels pour chaque post"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour servir les fichiers
@app.get("/files/{content_type}/{filename}")
async def serve_file(content_type: str, filename: str):
    """Sert les fichiers générés"""
    try:
        file_path = storage.get_file_path(filename, content_type)
        
        # Debug: afficher le chemin recherché
        print(f"Recherche du fichier: {file_path}")
        print(f"Le fichier existe: {file_path.exists()}")
        
        if file_path.exists():
            return FileResponse(file_path)
        else:
            # Lister les fichiers disponibles pour debug
            available_files = []
            storage_path = Path(LOCAL_STORAGE_PATH)
            if storage_path.exists():
                for folder in storage_path.iterdir():
                    if folder.is_dir():
                        for file in folder.iterdir():
                            if file.is_file():
                                available_files.append(f"{folder.name}/{file.name}")
            
            raise HTTPException(
                status_code=404, 
                detail={
                    "error": "Fichier non trouvé",
                    "requested_path": str(file_path),
                    "available_files": available_files[:10]  # Limiter à 10 fichiers
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

# Nouvel endpoint pour lister les fichiers disponibles
@app.get("/files")
async def list_files():
    """Liste tous les fichiers disponibles"""
    try:
        files_by_type = {}
        storage_path = Path(LOCAL_STORAGE_PATH)
        
        if not storage_path.exists():
            return {"message": "Dossier de stockage non trouvé", "path": str(storage_path)}
        
        for folder in storage_path.iterdir():
            if folder.is_dir():
                files_by_type[folder.name] = []
                for file in folder.iterdir():
                    if file.is_file():
                        files_by_type[folder.name].append({
                            "name": file.name,
                            "size": file.stat().st_size,
                            "url": f"{BASE_URL}/files/{folder.name}/{file.name}",
                            "created": datetime.fromtimestamp(file.stat().st_ctime).isoformat()
                        })
        
        return {
            "storage_path": str(storage_path),
            "total_folders": len(files_by_type),
            "files_by_type": files_by_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# Endpoint de santé
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "storage_path": LOCAL_STORAGE_PATH,
        "apis_configured": {
            "openai": bool(os.getenv('OPENAI_API_KEY')),
            "elevenlabs": bool(os.getenv('ELEVENLABS_API_KEY'))
        }
    }

@app.get("/debug/storage")
async def debug_storage():
    """Debug du système de stockage"""
    return {
        "LOCAL_STORAGE_PATH": LOCAL_STORAGE_PATH,
        "BASE_URL": BASE_URL,
        "storage_exists": Path(LOCAL_STORAGE_PATH).exists(),
        "storage_is_dir": Path(LOCAL_STORAGE_PATH).is_dir(),
        "storage_permissions": oct(Path(LOCAL_STORAGE_PATH).stat().st_mode)[-3:] if Path(LOCAL_STORAGE_PATH).exists() else "N/A",
        "folders": [f.name for f in Path(LOCAL_STORAGE_PATH).iterdir() if f.is_dir()] if Path(LOCAL_STORAGE_PATH).exists() else []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)