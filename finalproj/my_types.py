from enum import Enum, auto
from typing import Dict, List, TypedDict, Any

# Webhook Request Type
class ContextType(TypedDict):
  name: str
  lifespanCount: int
  parameters: Dict

class PartType(TypedDict):
  text: str
  entityType: str
  alias: str
  userDefined: bool

class TypeEnum(Enum):
  TYPE_UNSPECIFIED = auto()
  EXAMPLE = auto()
  TEMPLATE = auto()
  
class WebhookStateEnum(Enum):
  WEBHOOK_STATE_UNSPECIFIED = auto() 
  WEBHOOK_STATE_ENABLED = auto()
  WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING = auto()
  
class TrainingPhraseType(TypedDict):
  name: str
  type: TypeEnum
  parts: List[PartType]
  timesAddedCount: int

class ParameterType(TypedDict):
  name: str
  displayName: str
  value: str
  defaultValue: str
  entityTypeDisplayName: str
  mandatory: bool
  prompts: List[str]
  isList: bool

class PlatformEnum(Enum):
  PLATFORM_UNSPECIFIED = auto()
  FACEBOOK = auto()
  SLACK = auto()
  TELEGRAM = auto()
  KIK = auto()
  SKYPE = auto()
  LINE = auto()
  VIBER = auto()
  ACTIONS_ON_GOOGLE = auto()
  GOOGLE_HANGOUTS = auto()

class TextType(TypedDict):
  text: List[str]

class TextMessageType(TypedDict):
  platform: PlatformEnum
  text: TextType

class FollowupIntentInfo(TypedDict):
  followupIntentName: str
  parentFollowupIntentName: str
  
class IntentType(TypedDict):
  name: str
  displayName: str
  webhookState: WebhookStateEnum
  priority: int
  isFallback: bool
  mlDisabled: bool
  liveAgentHandoff: bool
  endInteraction: bool
  inputContextNames: List[str]
  events: List[str]
  trainingPhrases: List[TrainingPhraseType]
  action: str
  outputContexts: List[ContextType]
  resetContexts: bool
  parameters: List[ParameterType]
  messages: List[TextMessageType]
  defaultResponsePlatforms: List[PlatformEnum]
  rootFollowupIntentName: str
  parentFollowupIntentName: str
  followupIntentInfo: List[FollowupIntentInfo]

class SentimentType(TypedDict):
  score: int
  magnitude: int

class SentimentalAnalysisResultType(TypedDict):
  queryTextSentiment: SentimentType
  
class QueryResultType(TypedDict):
  queryText: str
  parameters: Dict[str, Any]
  allRequiredParamsPresent: bool
  cancelSlotFilling: bool
  fulfillmentText: str
  fulfillmentMessages: List[Dict[str, TextType]]
  webhookSource: str
  webhookPayload: Dict
  outputContexts: List[ContextType]
  intent: IntentType
  intentDetectionConfidence: int
  diagnosticInfo: Dict
  sentimentalAnalysisResult: SentimentalAnalysisResultType

class OriginalDetectIntentRequestType(TypedDict):
  source: str
  version: str
  payload: Dict
  
class WebhookRequestType(TypedDict):
  responseId: str
  session: str
  queryResult: QueryResultType
  originalDetectIntentRequest: OriginalDetectIntentRequestType


# Webhook Response Type
class EventInputType(TypedDict):
  name: str
  parameters: Dict
  languageCode: str

class EntityOverrideModeEnum(Enum):
  ENTITY_OVERRIDE_MODE_UNSPECIFIED = auto()
  ENTITY_OVERRIDE_MODE_OVERRIDE = auto()
  ENTITY_OVERRIDE_MODE_SUPPLEMENT = auto()

class EntityType(TypedDict):
  value: str
  synonyms: List[str]
  
class SessionEntityTypeType(TypedDict):
  name: str
  entityOverrideMode: EntityOverrideModeEnum
  entities: List[EntityType]
  
class WebhookResponseType(TypedDict):
  fulfillmentText: str

# class WebhookResponseType(TypedDict):
#   fulfillmentText: str
#   fulfillmentMessages: List[TextMessageType]
#   source: str
#   payload: Dict
#   outputContexts: List[ContextType]
#   followupEventInput: List[EventInputType]
#   sessionEntityTypes: List[SessionEntityTypeType]