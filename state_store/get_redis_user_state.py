import logging
import sys
from .redis_state_store import RedisStateStore
from .user_identity import UserIdentity

# Set higher logging level for debugging Redis issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_redis_user_state(user_id: str, is_app_home: bool, redis_url: str = None):
    """
    Get user state from Redis
    
    Args:
        user_id: The user ID
        is_app_home: Whether the request is from app home
        redis_url: Optional Redis URL. If not provided, uses REDIS_URL env variable
    
    Returns:
        Tuple of (provider_name, model_name) or (None, None) if not found
    """
    print(f"🔍 Fetching Redis state for user: {user_id}")
    
    try:
        redis_store = RedisStateStore(redis_url=redis_url)
        user_data = redis_store.get_state(user_id)
        
        if not user_data:
            if not is_app_home:
                print(f"❌ No provider selection found for user: {user_id} (non-app-home context)")
                raise FileNotFoundError("No provider selection found. Please navigate to the App Home and make a selection.")
            print(f"ℹ️ No state found in Redis for user: {user_id}")
            return None, None
        
        user_identity: UserIdentity = user_data
        provider = user_identity.get("provider")
        model = user_identity.get("model")
        
        print(f"✅ Found Redis state for user {user_id}: provider={provider}, model={model}")
        return provider, model
        
    except FileNotFoundError as e:
        # Re-raise FileNotFoundError for expected flow control
        raise e
    except Exception as e:
        error_msg = f"❌ Error getting Redis state for user {user_id}: {e}"
        print(error_msg, file=sys.stderr)
        logger.error(error_msg)
        return None, None 