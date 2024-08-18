import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "../backend/schema.yml",
  output: {
    path: "js/api",
  },
  client: "axios",
  useOptions: true,
});