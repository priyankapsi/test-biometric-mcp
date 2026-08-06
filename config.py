from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Base URL of the actual running "BioMatrixReport" app (NOT the git repo
    # URL) - this is where every generated tool sends its HTTP requests.
    # Detected from the source repo as a suggestion only - confirm it's correct.
    target_app_base_url: str = "http://localhost:5183"

    port: int = 8000

    # Only used when this server itself is reachable at a public URL, to
    # build OAuth redirect_uris. Set this AFTER your first deploy once you
    # know the public URL (see README).
    public_base_url: str = ""



settings = Settings()
