# Local Langfuse Docker Compose

This folder contains a complete local Langfuse stack for development.

## Services Included

- `langfuse-web` (UI + API) on `http://localhost:3000`
- `langfuse-worker`
- `postgres`
- `clickhouse`
- `redis`
- `minio` (S3-compatible storage) on `http://localhost:9090`
- `minio console` on `http://localhost:9091`

## Important: Single-Node ClickHouse Mode

This setup runs ClickHouse in single-node mode.
`CLICKHOUSE_CLUSTER_ENABLED=false` is required to avoid ZooKeeper/ReplicatedMergeTree migrations.

## Start

```powershell
cd references\projects\multi_agent_langfuse\deploy\langfuse
Copy-Item .env.example .env
```

Generate required secrets (especially 64-hex `ENCRYPTION_KEY`):

```powershell
$enc = -join ((1..64) | % { '{0:x}' -f (Get-Random -Minimum 0 -Maximum 16) })
$salt = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
$next = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')

(Get-Content .env) |
  % { $_ -replace '^ENCRYPTION_KEY=.*$', "ENCRYPTION_KEY=$enc" } |
  % { $_ -replace '^SALT=.*$', "SALT=$salt" } |
  % { $_ -replace '^NEXTAUTH_SECRET=.*$', "NEXTAUTH_SECRET=$next" } |
  Set-Content .env

docker compose up -d
```

## Verify

```powershell
docker compose ps
docker compose logs -f langfuse-web
```

Open `http://localhost:3000`, create a project, and generate API keys.

## Connect Your Multi-Agent Project

In workspace `.env` (root), set:

```env
LANGFUSE_PUBLIC_KEY=your_public_key_from_local_ui
LANGFUSE_SECRET_KEY=your_secret_key_from_local_ui
LANGFUSE_HOST=http://localhost:3000
```

## Stop

```powershell
docker compose down
```

To remove persisted data too:

```powershell
docker compose down -v
```

## If You Already Hit the ZooKeeper Error

Restart cleanly so migrations run again in non-cluster mode:

```powershell
docker compose down -v
docker compose up -d
```

## If You See `fillFromDate` ClickHouse Dashboard Errors

Use a clean rebuild to remove stale DB/UI state and pull current images:

```powershell
docker compose down -v
docker compose pull
docker compose up -d
```

Then hard-refresh the browser (or open Langfuse in an incognito window) and recheck.

If trace export logs show `Failed to upload JSON to S3`, verify:
- `LANGFUSE_S3_MEDIA_UPLOAD_ENDPOINT=http://minio:9000` in `deploy/langfuse/.env`
- `minio-create-bucket` completed successfully:
```powershell
docker compose logs minio-create-bucket
```

## Security Note

The default example credentials are for local development only.
For any shared environment, replace all secrets before running.
