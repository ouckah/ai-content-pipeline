"""
Simple AI Agent with Tools
Basic AI agent that can use tools and chat with users.
"""

import os
from typing import Dict, List, Any
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()


class Tool:
    """Base class for tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, **kwargs) -> str:
        """Execute the tool and return result as string."""
        raise NotImplementedError


class TextGenerationTool(Tool):
    """Tool for text generation and writing tasks."""
    
    def __init__(self):
        super().__init__("text", "Generate, rewrite, and brainstorm text content")
    
    def execute(self, task: str, content: str = "", style: str = "professional") -> str:
        """Execute text generation tasks."""
        if task == "generate":
            return f"Generated {style} content: {content}"
        elif task == "rewrite":
            return f"Rewritten in {style} style: {content}"
        elif task == "brainstorm":
            return f"Brainstorming ideas for: {content}"
        elif task == "research":
            return f"Research summary for: {content}"
        else:
            return f"Unknown text task: {task}"


class ImageGenerationTool(Tool):
    """Tool for AI-powered image generation and editing."""
    
    def __init__(self):
        super().__init__("image", "Generate and edit images using AI")
    
    def execute(self, action: str, prompt: str = "", style: str = "realistic") -> str:
        """Execute image generation tasks."""
        if action == "generate":
            return f"Generated {style} image: '{prompt}' (placeholder - integrate with DALL-E/Midjourney)"
        elif action == "edit":
            return f"Edited image with prompt: '{prompt}'"
        elif action == "thumbnail":
            return f"Created thumbnail for: '{prompt}'"
        else:
            return f"Unknown image action: {action}"


class VideoGenerationTool(Tool):
    """Tool for video generation and editing."""
    
    def __init__(self):
        super().__init__("video", "Generate videos from text and images")
    
    def execute(self, action: str, content: str = "", duration: str = "30s") -> str:
        """Execute video generation tasks."""
        if action == "text_to_video":
            return f"Generated {duration} video from text: '{content}' (placeholder - integrate with Google Veo 3/Synthesia)"
        elif action == "animate":
            return f"Animated image/avatar: '{content}'"
        elif action == "edit":
            return f"Edited video: '{content}'"
        else:
            return f"Unknown video action: {action}"


class AudioTool(Tool):
    """Tool for text-to-speech and audio generation."""
    
    def __init__(self):
        super().__init__("audio", "Generate speech and audio content")
    
    def execute(self, action: str, text: str = "", voice: str = "default") -> str:
        """Execute audio generation tasks."""
        if action == "tts":
            return f"Generated {voice} voice audio: '{text}' (placeholder - integrate with ElevenLabs/OpenAI TTS)"
        elif action == "podcast":
            return f"Created podcast segment: '{text}'"
        elif action == "audiobook":
            return f"Generated audiobook narration: '{text}'"
        else:
            return f"Unknown audio action: {action}"


class ContentWorkflowTool(Tool):
    """Tool for content planning and workflow management."""
    
    def __init__(self):
        super().__init__("workflow", "Manage content calendar and project workflows")
    
    def execute(self, action: str, content: str = "", date: str = "") -> str:
        """Execute workflow management tasks."""
        if action == "plan":
            return f"Created content plan: '{content}'"
        elif action == "schedule":
            return f"Scheduled content for {date}: '{content}'"
        elif action == "collaborate":
            return f"Set up collaboration for: '{content}'"
        elif action == "review":
            return f"Content review cycle started for: '{content}'"
        else:
            return f"Unknown workflow action: {action}"


class SEOTool(Tool):
    """Tool for SEO optimization and content analysis."""
    
    def __init__(self):
        super().__init__("seo", "Optimize content for search engines")
    
    def execute(self, action: str, content: str = "", keywords: str = "") -> str:
        """Execute SEO optimization tasks."""
        if action == "optimize":
            return f"SEO optimized content for keywords '{keywords}': {content}"
        elif action == "analyze":
            return f"SEO analysis for: '{content}'"
        elif action == "keywords":
            return f"Keyword research for: '{content}'"
        elif action == "meta":
            return f"Generated meta description for: '{content}'"
        else:
            return f"Unknown SEO action: {action}"


class SocialMediaTool(Tool):
    """Tool for social media distribution and management."""
    
    def __init__(self):
        super().__init__("social", "Manage social media posting and analytics")
    
    def execute(self, action: str, content: str = "", platform: str = "all") -> str:
        """Execute social media tasks."""
        if action == "post":
            return f"Posted to {platform}: '{content}'"
        elif action == "schedule":
            return f"Scheduled post for {platform}: '{content}'"
        elif action == "analytics":
            return f"Analytics report for {platform}: '{content}'"
        elif action == "hashtags":
            return f"Generated hashtags for: '{content}'"
        else:
            return f"Unknown social media action: {action}"


class AIAgent:
    """Simple AI agent with tool support."""
    
    def __init__(self, name: str = "AI Agent"):
        self.name = name
        self.tools: Dict[str, Tool] = {}
        self.messages: List[Dict[str, str]] = []
        
        # Get API key from environment
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        # Configure Gemini if key is available
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
        
        # Register all content creation tools
        self.add_tool(TextGenerationTool())
        self.add_tool(ImageGenerationTool())
        self.add_tool(VideoGenerationTool())
        self.add_tool(AudioTool())
        self.add_tool(ContentWorkflowTool())
        self.add_tool(SEOTool())
        self.add_tool(SocialMediaTool())
        
        print(f"Initialized {self.name}")
        if self.gemini_key:
            print("✓ Gemini API key found")
        if self.openai_key:
            print("✓ OpenAI API key found")
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent."""
        self.tools[tool.name] = tool
        print(f"Added tool: {tool.name}")
    
    def use_tool(self, tool_name: str, **kwargs) -> str:
        """Use a tool and return the result."""
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found"
        
        tool = self.tools[tool_name]
        print(f"Using tool: {tool_name}")
        return tool.execute(**kwargs)
    
    def chat(self, message: str) -> str:
        """Process a chat message."""
        self.messages.append({"role": "user", "content": message})
        
        if self.model:
            try:
                # Create context with conversation history and available tools
                tools_description = '\n'.join([f"- {name}: {tool.description}" for name, tool in self.tools.items()])
                
                context = f"""You are an AI content creation assistant with access to powerful tools. When a user requests something that would benefit from using a tool, automatically use it by including the tool call in your response.

Available Tools:
{tools_description}

IMPORTANT: When you decide to use a tool, format it as: TOOL_CALL[tool_name:parameter1=value1,parameter2=value2]

Examples:
- User asks "search for weather in London" → Use: TOOL_CALL[search:query=weather in London]
- User asks "create a blog post about AI" → Use: TOOL_CALL[text:task=generate,content=blog post about AI]
- User asks "make an image of a sunset" → Use: TOOL_CALL[image:action=generate,prompt=sunset]
- User asks "read my notes.txt file" → Use: TOOL_CALL[file:action=read,path=notes.txt]

Always be helpful and proactive. If a user's request can be fulfilled with a tool, use it automatically. Provide context about what you're doing and why.

Conversation History:
"""
                # Add recent messages to context
                for msg in self.messages[-5:]:  # Last 5 messages for context
                    context += f"{msg['role']}: {msg['content']}\n"
                
                # Generate response using Gemini
                response = self.model.generate_content(context + f"\nUser: {message}\nAssistant:")
                ai_response = response.text.strip()
                
                # Check if the response contains tool calls and execute them
                ai_response = self._process_tool_calls(ai_response)
                
            except Exception as e:
                ai_response = f"Error with Gemini API: {str(e)}\nAvailable tools: {', '.join(self.tools.keys())}"
        else:
            # Fallback if no API key
            tools_list = ", ".join(self.tools.keys())
            ai_response = f"No API key configured. Available tools: {tools_list}"
        
        self.messages.append({"role": "assistant", "content": ai_response})
        return ai_response
    
    def _process_tool_calls(self, response: str) -> str:
        """Process and execute tool calls in the AI response."""
        import re
        
        # Find all tool calls in the format TOOL_CALL[tool_name:param1=value1,param2=value2]
        tool_pattern = r'TOOL_CALL\[([^:]+):([^\]]+)\]'
        matches = re.findall(tool_pattern, response)
        
        processed_response = response
        
        for tool_name, params_str in matches:
            try:
                # Parse parameters
                params = {}
                if params_str.strip():
                    for param_pair in params_str.split(','):
                        if '=' in param_pair:
                            key, value = param_pair.split('=', 1)
                            params[key.strip()] = value.strip()
                
                # Execute the tool
                result = self.use_tool(tool_name.strip(), **params)
                
                # Replace the tool call with the result
                tool_call_text = f"TOOL_CALL[{tool_name}:{params_str}]"
                processed_response = processed_response.replace(
                    tool_call_text, 
                    f"\n**Tool Result ({tool_name}):** {result}\n"
                )
                
            except Exception as e:
                # Replace with error message
                tool_call_text = f"TOOL_CALL[{tool_name}:{params_str}]"
                processed_response = processed_response.replace(
                    tool_call_text, 
                    f"\n**Tool Error ({tool_name}):** {str(e)}\n"
                )
        
        return processed_response
    
    def run(self) -> None:
        """Run interactive chat."""
        print(f"\n{self.name} started. Type 'quit' to exit.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Check for tool commands
                if user_input.startswith("/"):
                    parts = user_input[1:].split()
                    if parts:
                        tool_name = parts[0]
                        
                        # File tool
                        if tool_name == "file" and len(parts) >= 3:
                            action, path = parts[1], parts[2]
                            content = " ".join(parts[3:]) if len(parts) > 3 else ""
                            result = self.use_tool("file", action=action, path=path, content=content)
                            print(f"Tool result: {result}")
                        
                        # Search tool
                        elif tool_name == "search" and len(parts) >= 2:
                            query = " ".join(parts[1:])
                            result = self.use_tool("search", query=query)
                            print(f"Tool result: {result}")
                        
                        # Text generation tool
                        elif tool_name == "text" and len(parts) >= 2:
                            task = parts[1]
                            content = " ".join(parts[2:]) if len(parts) > 2 else ""
                            result = self.use_tool("text", task=task, content=content)
                            print(f"Tool result: {result}")
                        
                        # Image generation tool
                        elif tool_name == "image" and len(parts) >= 2:
                            action = parts[1]
                            prompt = " ".join(parts[2:]) if len(parts) > 2 else ""
                            result = self.use_tool("image", action=action, prompt=prompt)
                            print(f"Tool result: {result}")
                        
                        # Video generation tool
                        elif tool_name == "video" and len(parts) >= 2:
                            action = parts[1]
                            content = " ".join(parts[2:]) if len(parts) > 2 else ""
                            result = self.use_tool("video", action=action, content=content)
                            print(f"Tool result: {result}")
                        
                        # Audio tool
                        elif tool_name == "audio" and len(parts) >= 2:
                            action = parts[1]
                            text = " ".join(parts[2:]) if len(parts) > 2 else ""
                            result = self.use_tool("audio", action=action, text=text)
                            print(f"Tool result: {result}")
                        
                        # Workflow tool
                        elif tool_name == "workflow" and len(parts) >= 2:
                            action = parts[1]
                            content = " ".join(parts[2:]) if len(parts) > 2 else ""
                            result = self.use_tool("workflow", action=action, content=content)
                            print(f"Tool result: {result}")
                        
                        # SEO tool
                        elif tool_name == "seo" and len(parts) >= 2:
                            action = parts[1]
                            content = " ".join(parts[2:]) if len(parts) > 2 else ""
                            result = self.use_tool("seo", action=action, content=content)
                            print(f"Tool result: {result}")
                        
                        # Social media tool
                        elif tool_name == "social" and len(parts) >= 2:
                            action = parts[1]
                            content = " ".join(parts[2:]) if len(parts) > 2 else ""
                            result = self.use_tool("social", action=action, content=content)
                            print(f"Tool result: {result}")
                        
                        else:
                            print("Available tools:")
                            print("  /file read|write|list <path> [content]")
                            print("  /search <query>")
                            print("  /text generate|rewrite|brainstorm|research <content>")
                            print("  /image generate|edit|thumbnail <prompt>")
                            print("  /video text_to_video|animate|edit <content>")
                            print("  /audio tts|podcast|audiobook <text>")
                            print("  /workflow plan|schedule|collaborate|review <content>")
                            print("  /seo optimize|analyze|keywords|meta <content>")
                            print("  /social post|schedule|analytics|hashtags <content>")
                else:
                    response = self.chat(user_input)
                    print(f"Agent: {response}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


# Example usage
if __name__ == "__main__":
    agent = AIAgent("Content Agent")
    agent.run()