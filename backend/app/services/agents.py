# app/services/agents.py
from app.services.nim_service import nim_service
from app.services.vector_store import vector_store
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

# Set up logging
logger = logging.getLogger(__name__)

class DataRetrievalAgent:
    async def retrieve_context(self, query: str) -> str:
        """Agent 1: Retrieve relevant context from data center knowledge base"""
        logger.info(f"🔍 DataRetrievalAgent searching for: {query}")
        
        try:
            results = await vector_store.search(query, n_results=5)
            
            context = ""
            if results.get('documents') and results['documents'][0]:
                context += "📚 RELEVANT DATA CENTER KNOWLEDGE:\n\n"
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results.get('metadatas') and results['metadatas'][0] else {}
                    source = metadata.get('source', 'operational_knowledge')
                    doc_type = metadata.get('type', 'technical_data')
                    context += f"📄 Source: {source} | Type: {doc_type}\n{doc}\n\n"
                
                logger.info(f"✅ Retrieved {len(results['documents'][0])} relevant documents")
            else:
                context = "ℹ️ No specific data center knowledge found for this query. Using general data center operational expertise."
                logger.warning("No documents found in vector store for query")
            
            return context
            
        except Exception as e:
            logger.error(f"❌ Data retrieval failed: {e}")
            return f"⚠️ Knowledge base temporarily unavailable. Proceeding with general data center expertise.\nError: {str(e)}"

class ReasoningAgent:
    async def analyze_issue(self, query: str, context: str) -> Dict[str, Any]:
        """Agent 2: Analyze and identify root causes for data center operations"""
        logger.info(f"🤔 ReasoningAgent analyzing: {query}")
        
        system_prompt = """You are a senior data center operations expert with 15+ years of experience."""
        
        prompt = f"""## DATA CENTER OPERATIONAL ANALYSIS

QUERY: {query}

CONTEXT:
{context if context else "No specific context available"}

ANALYSIS REQUESTED:
1. Identify 2-4 specific technical root causes
2. Assess severity level (Critical/High/Medium/Low)
3. Estimate time to failure if applicable
4. List affected systems
5. Provide confidence score

RESPONSE FORMAT (JSON):
{{
    "root_causes": ["cause1", "cause2"],
    "severity": "High with justification",
    "time_to_failure_hours": 48,
    "affected_systems": ["Cooling", "Power"],
    "confidence_score": 0.85
}}"""
        
        try:
            response = await nim_service.generate_completion(prompt, system_prompt)
            analysis_text = response['choices'][0]['message']['content']
            logger.info("✅ Reasoning analysis completed")
            
            # Parse JSON from response
            analysis = self._parse_json_response(analysis_text)
            
            # Validate required fields
            required_fields = ['root_causes', 'severity', 'affected_systems', 'confidence_score']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = self._get_fallback_value(field)
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Reasoning analysis failed: {e}")
            return self._get_fallback_analysis(query)

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse JSON from model response with robust error handling"""
        try:
            clean_text = text.strip()
            
            # Extract JSON from markdown code blocks if present
            if '```json' in clean_text:
                clean_text = clean_text.split('```json')[1].split('```')[0].strip()
            elif '```' in clean_text:
                clean_text = clean_text.split('```')[1].strip()
            
            # Parse JSON
            return json.loads(clean_text)
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed, using text analysis: {e}")
            return {
                "root_causes": ["Analysis completed but formatting issue occurred"],
                "severity": "Medium",
                "time_to_failure_hours": None,
                "affected_systems": ["Multiple systems"],
                "confidence_score": 0.6,
                "raw_analysis": text
            }

    def _get_fallback_value(self, field: str) -> Any:
        """Provide fallback values for missing required fields"""
        fallbacks = {
            'root_causes': ['Further investigation required'],
            'severity': 'Medium',
            'affected_systems': ['Data center infrastructure'],
            'confidence_score': 0.5
        }
        return fallbacks.get(field, 'Unknown')

    def _get_fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Provide comprehensive fallback analysis"""
        return {
            "root_causes": ["System analysis temporarily unavailable"],
            "severity": "Medium",
            "time_to_failure_hours": None,
            "affected_systems": ["Data center operations"],
            "confidence_score": 0.3
        }

class ActionPlanningAgent:
    async def create_action_plan(self, analysis: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Agent 3: Create actionable plan with ROI calculations"""
        logger.info(f"📋 ActionPlanningAgent creating plan")
        
        system_prompt = """You are a data center financial and operations planner."""
        
        # Create analysis summary safely
        analysis_summary = f"""
Root Causes: {', '.join(analysis.get('root_causes', ['Analysis in progress']))}
Severity: {analysis.get('severity', 'Medium')}
Affected Systems: {', '.join(analysis.get('affected_systems', ['Infrastructure']))}
Confidence: {analysis.get('confidence_score', 0.5) * 100:.1f}%
"""
        
        prompt = f"""## DATA CENTER ACTION PLAN

QUERY: {query}

ANALYSIS:
{analysis_summary}

CREATE ACTION PLAN WITH:
1. Immediate actions (next 24 hours)
2. Short-term solutions (1-4 weeks)
3. Long-term recommendations (1-6 months)
4. ROI calculation with cost savings

RESPONSE FORMAT (JSON):
{{
    "immediate_actions": ["action1", "action2"],
    "short_term_solutions": ["solution1", "solution2"],
    "long_term_recommendations": ["recommendation1"],
    "roi_analysis": "ROI explanation",
    "estimated_cost_savings": 125000
}}"""
        
        try:
            response = await nim_service.generate_completion(prompt, system_prompt)
            plan_text = response['choices'][0]['message']['content']
            logger.info("✅ Action plan created")
            
            # Parse JSON from response
            plan = self._parse_action_plan_response(plan_text)
            
            # Ensure required fields
            if 'estimated_cost_savings' not in plan:
                plan['estimated_cost_savings'] = self._calculate_estimated_savings(analysis)
                
            return plan
            
        except Exception as e:
            logger.error(f"❌ Action planning failed: {e}")
            return self._get_fallback_action_plan()

    def _parse_action_plan_response(self, text: str) -> Dict[str, Any]:
        """Parse action plan JSON with error handling"""
        try:
            clean_text = text.strip()
            
            if '```json' in clean_text:
                clean_text = clean_text.split('```json')[1].split('```')[0].strip()
            elif '```' in clean_text:
                clean_text = clean_text.split('```')[1].strip()
                
            return json.loads(clean_text)
            
        except json.JSONDecodeError as e:
            logger.warning(f"Action plan JSON parsing failed: {e}")
            return self._get_fallback_action_plan()

    def _calculate_estimated_savings(self, analysis: Dict[str, Any]) -> int:
        """Calculate estimated savings based on severity"""
        severity_multipliers = {
            'Critical': 200000,
            'High': 125000,
            'Medium': 75000,
            'Low': 25000
        }
        
        severity = analysis.get('severity', 'Medium').split(' ')[0]
        return severity_multipliers.get(severity, 75000)

    def _get_fallback_action_plan(self) -> Dict[str, Any]:
        """Provide fallback action plan"""
        return {
            "immediate_actions": ["Review analysis", "Consult team"],
            "short_term_solutions": ["Schedule assessment"],
            "long_term_recommendations": ["Consider upgrades"],
            "estimated_cost_savings": 50000
        }

class AgentOrchestrator:
    def __init__(self):
        self.retrieval_agent = DataRetrievalAgent()
        self.reasoning_agent = ReasoningAgent()
        self.planning_agent = ActionPlanningAgent()
        logger.info("🎯 AgentOrchestrator initialized")

    async def process_query(self, query: str) -> Dict[str, Any]:
        """Orchestrate the three agents"""
        logger.info(f"🚀 Processing query: '{query}'")
        
        try:
            # Agent 1: Data Retrieval
            context = await self.retrieval_agent.retrieve_context(query)
            
            # Agent 2: Reasoning
            analysis = await self.reasoning_agent.analyze_issue(query, context)
            
            # Agent 3: Action Planning
            action_plan = await self.planning_agent.create_action_plan(analysis, query)
            
            result = {
                "query": query,
                "context_used": context,
                "analysis": analysis,
                "action_plan": action_plan,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            logger.info(f"✅ Successfully processed query")
            return result
            
        except Exception as e:
            logger.error(f"❌ Agent orchestration failed: {e}")
            return {
                "query": query,
                "error": True,
                "error_message": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }