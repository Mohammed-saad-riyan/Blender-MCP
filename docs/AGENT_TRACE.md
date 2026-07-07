# Agent Trace Evidence

Use this document to capture a reproducible Blender MCP run.

## Scenario

Goal: create a product-style scene containing a metallic cube, a three-point lighting setup and a camera, then verify the final scene.

Agent: `<provider/model>`

Blender: `<version>`

Commit: `<git sha>`

## Trace

### User request

```text
Create a metallic cube centered at the origin, add a three-point lighting setup,
frame it with a camera, and verify that the final scene matches the request.
```

### Tool discovery

Paste the captured list of available tools here.

### Plan

```text
1. Inspect current scene.
2. Create or locate the target cube.
3. Create and assign a metallic material.
4. Create key, fill and rim lights.
5. Position camera.
6. Capture viewport.
7. Verify object state and spatial context.
```

### Tool calls

For each call, record the tool name, arguments and structured result.

### Failure and recovery

If a genuine recoverable failure occurs, record the first attempt, the returned error, what the agent inspected, the changed arguments, and the successful retry. Do not manufacture a failure for documentation.

### Verification

Paste the final verification result, including issues, suggestions, spatial context and viewport evidence.

## Evidence checklist

- [ ] natural-language request is visible
- [ ] tool discovery is visible
- [ ] tool arguments and results are visible
- [ ] Blender viewport visibly changes
- [ ] genuine recovery is captured if one occurs
- [ ] final verification output is visible
- [ ] final scene is shown clearly

## Demo asset

Save the compressed demo at `docs/assets/blender-mcp-demo.gif`. A higher-resolution video can also be linked from the main README.