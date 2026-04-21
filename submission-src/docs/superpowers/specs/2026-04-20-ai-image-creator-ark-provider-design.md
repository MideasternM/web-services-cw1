# AI Image Creator Ark Provider Design

**Goal:** Extend the installed `ai-image-creator` skill so it can generate images through ByteDance Volcano Engine Ark as a first-class provider, using `ARK_API_KEY` for authentication and `doubao-seedream-5-0-260128` as the default Ark model.

**Target outcome:** Preserve the existing skill workflow while adding a clean `--provider ark` path that is explicit, documented, and safe to use without storing credentials in code or documentation.

## 1. Problem Definition

The installed `ai-image-creator` skill currently supports direct generation through OpenRouter and Google AI Studio. The user wants one more image-generation platform added to the same workflow rather than a separate script or ad hoc local snippet. The requested backend is Volcano Engine Ark, and the desired model is `doubao-seedream-5-0-260128`.

This is a provider-level change rather than a mere new model alias. Ark has its own base URL, authentication variable, and request/response shape. Treating it as a real provider keeps the CLI honest and avoids hiding backend-specific behavior under existing OpenRouter or Google branches.

## 2. Scope

### In scope

- Add `ark` as a supported `--provider` value in the installed skill script.
- Add direct Ark authentication through the `ARK_API_KEY` environment variable.
- Default Ark generation to `doubao-seedream-5-0-260128`.
- Support text-to-image generation through Ark using the same CLI entrypoint as the existing providers.
- Support the user-provided Ark semantics where generation requests return an image URL and include `watermark=True`.
- Download the generated image from the returned URL and save it through the skill's existing output pipeline.
- Update skill documentation so Ark setup and Ark command examples are explicit.
- Add verification for provider routing and non-secret configuration handling.

### Out of scope

- Hardcoding the user's API key into any file.
- Replacing existing OpenRouter or Google behavior.
- Adding every Ark model or every Ark API capability in the first pass.
- Full multimodal editing support for Ark reference images unless the current Ark image endpoint clearly supports it in the same flow.
- Image analysis through Ark unless the endpoint shape and response contract are already proven compatible.

## 3. Approaches Considered

### Option A: First-class `ark` provider

Add Ark as a new provider branch across argument parsing, model resolution, credential detection, URL construction, request building, response parsing, and output download.

This is the recommended approach. It matches the user's wording of "add another platform", keeps the command surface explicit, and avoids misleading credential or endpoint assumptions.

### Option B: Treat Ark as just another model under OpenRouter

This would require less code, but it does not satisfy the requirement because it routes through OpenRouter rather than Ark directly. It also ties the behavior to the wrong credential source.

### Option C: Add a hidden Ark special case inside existing provider logic

This would make the change appear smaller, but the CLI and internal structure would become harder to reason about. Provider-specific behavior would be obscured and future maintenance would be worse.

## 4. Selected Design

The skill will add Ark as a first-class provider named `ark`.

Primary usage will be:

```bash
uv run python ${CLAUDE_SKILL_DIR}/scripts/generate-image.py \
  --provider ark \
  -m doubao-seedream-5-0-260128 \
  -p "Prompt text" \
  -o "output.png"
```

If `--provider ark` is used without `--model`, the script will default to `doubao-seedream-5-0-260128`.

The authentication source for Ark will be:

```text
ARK_API_KEY
```

The direct API base URL will be:

```text
https://ark.cn-beijing.volces.com/api/v3
```

The initial Ark request contract will follow the user-provided example closely:

- use the image generation endpoint semantics exposed through the existing HTTP client flow
- request `response_format="url"`
- set `watermark=True`
- accept `size` when `--image-size` is provided

The returned image URL will be fetched by the script and the binary image data will then continue through the existing save and optional post-processing pipeline.

## 5. Architecture Changes

The implementation will preserve the script's current provider-oriented structure. Each existing helper that branches on provider will receive an Ark branch where appropriate.

### 5.1 Argument parsing

- extend `--provider` choices to include `ark`
- update help text to mention Ark explicitly
- keep the rest of the CLI stable so the skill workflow remains familiar

### 5.2 Configuration and credential detection

- add `ARK_API_KEY` as a recognized environment variable
- Ark will use direct mode only in the first version
- existing Cloudflare AI Gateway detection will continue to apply only to OpenRouter and Google
- if `--provider ark` is selected and `ARK_API_KEY` is missing, the script will fail with a provider-specific setup error

### 5.3 Model resolution

- extend default provider mapping so `ark` resolves to `doubao-seedream-5-0-260128`
- allow the explicit full model ID to pass through unchanged
- include a human-readable model description in `--list-models` output where practical

### 5.4 URL and header construction

- add an Ark direct URL builder targeting the Ark image generation route under the `api/v3` base path
- send standard JSON headers plus bearer authorization using `ARK_API_KEY`
- keep secret masking in debug logs

### 5.5 Request body construction

For the first Ark version, the request body will support:

- `model`
- `prompt`
- `response_format="url"`
- `size` when `--image-size` is provided
- `extra_body={"watermark": true}`

Unsupported flags for Ark will fail fast with a clear message. This avoids pretending that all provider features are interchangeable.

### 5.6 Response parsing and image download

Ark is expected to return an image URL rather than base64 image data. The script will therefore:

- parse the Ark response for the first image URL
- download the resulting image bytes with the standard library HTTP client
- feed those bytes into the same output-writing path already used after provider extraction

This keeps file output, prompt metadata, and cost logging behavior as consistent as possible with the existing providers.

## 6. Feature Compatibility Rules

The first-pass compatibility contract will be explicit.

### Supported with Ark

- text-to-image generation
- `--provider ark`
- explicit Ark model ID or Ark default model
- `--image-size`
- standard output file saving

### Not supported initially with Ark

- `--analyze`
- `--ref`
- `--aspect-ratio` unless Ark documentation confirms a direct equivalent in the chosen endpoint
- Cloudflare gateway routing

If the user invokes unsupported combinations with `--provider ark`, the script should return a clear validation error before making a request.

## 7. Documentation Changes

The following installed skill files will be updated:

- `SKILL.md`
- `references/setup-guide.md`

Documentation changes will include:

- Ark listed as a supported provider
- `ARK_API_KEY` added to setup instructions
- an Ark example command using `doubao-seedream-5-0-260128`
- a short note that Ark support is currently generation-only in this skill

The user's API key will not be written into examples or config files.

## 8. Verification Strategy

Verification will focus on confidence without leaking secrets.

- syntax-check the modified Python script
- verify `--list-models` and provider help output
- exercise provider validation paths for Ark unsupported options
- if the local shell environment is configured safely, run one live Ark generation using `ARK_API_KEY` from the environment and confirm that the output file is created

If live verification is not possible, the implementation must still prove that provider routing, request assembly, and response handling are syntactically valid and internally consistent.

## 9. Risks and Mitigations

### Risk: Ark response shape differs from the user sample abstraction

Mitigation: isolate Ark response parsing in its own branch and validate against actual returned JSON before claiming feature completion.

### Risk: Reusing existing provider assumptions causes hidden regressions

Mitigation: keep Ark as a separate provider branch rather than forcing it through OpenRouter or Google code paths.

### Risk: Unsupported flags create confusing partial behavior

Mitigation: reject unsupported Ark flag combinations explicitly and document the supported surface clearly.

### Risk: Credentials are accidentally exposed in logs or files

Mitigation: continue masked logging only, rely on environment variables, and never embed the provided key into the repository or skill files.

## 10. Scope Boundary

This design covers only the installed `ai-image-creator` skill integration for Ark image generation. It does not redesign the coursework project, add a new standalone image tool, or expand Ark support beyond the minimum reliable workflow needed for provider-based image generation.
