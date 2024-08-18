const path = require("path");

const ReactRefreshWebpackPlugin = require("@pmmmwh/react-refresh-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = (env, argv) => {
  const isDev =  argv.mode === "development";
  const nodeModulesDir = path.resolve(__dirname, "node_modules");
  const localhostOutput = {
    path: path.resolve("./webpack_bundles/"),
    publicPath: "http://localhost:3000/frontend/webpack_bundles/",
    filename: "[name].js",
  };
  const productionOutput = {
    path: path.resolve("./webpack_bundles/"),
    publicPath: "auto",
    filename: "[name]-[chunkhash].js",
  };

  return {
    mode: isDev ? "development" : "production",
    devtool: "source-map",
    devServer: {
      hot: true,
      historyApiFallback: true,
      host: "0.0.0.0",
      port: 3000,
      // Allow CORS requests from the Django dev server domain:
      headers: { "Access-Control-Allow-Origin": "*" },
    },
    context: __dirname,
    entry: ["./src/index.tsx"],
    output: isDev ? localhostOutput : productionOutput,
    module: {
      rules: [
        {
          test: /\.(js|mjs|jsx|ts|tsx)$/,
          use: {
            loader: "swc-loader",
          },
        },
        {
          test: /\.css$/i,
          include: path.resolve(__dirname, 'src'),
          use: ['style-loader', 'css-loader', 'postcss-loader'],
        },
        {
          test: /\.(svg)(\?v=\d+\.\d+\.\d+)?$/,
          type: "asset",
        },
        {
          test: /\.(woff(2)?|eot|ttf|otf)(\?v=\d+\.\d+\.\d+)?$/,
          type: "asset",
        },
        {
          test: /\.(png|jpg|jpeg|gif|webp)?$/,
          type: "asset",
        },
      ],
    },
    plugins: [
      isDev && new ReactRefreshWebpackPlugin(),
      new BundleTracker({
        path: __dirname,
        filename: "webpack-stats.json",
      }),
    ].filter(Boolean),
    resolve: {
      modules: [nodeModulesDir, path.resolve(__dirname, "src")],
      extensions: [".js", ".jsx", ".ts", ".tsx"],
      alias: {
        '@': path.resolve(__dirname, 'src/vendor'),
      },
    },
    optimization: {
      minimize: !isDev,
      splitChunks: {
        // include all types of chunks
        chunks: "all",
      },
    },
  };
};