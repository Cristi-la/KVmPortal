import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  // input: "backend/schema.yml",
  input: "http://web:8000/api/schema/",
  output: {
    path: "src/vendor/api",
    format: "prettier",
  },
  timeout: 90,
  retryFor: 3, 
  client: "axios",
  useOptions: true,
});