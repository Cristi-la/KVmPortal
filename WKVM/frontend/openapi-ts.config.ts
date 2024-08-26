import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  // input: "backend/schema.yml",
  input: "http://localhost:8000/api/schema/",
  output: {
    path: "src/vendor/api",
    format: "prettier",
  },
  client: "axios",
  useOptions: true,
});