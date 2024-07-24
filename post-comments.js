import { Octokit } from "@octokit/rest";
import fs from "fs";
import path from "path";

async function postComments() {
  const token = process.env.GITHUB_TOKEN;
  const octokit = new Octokit({ auth: token });
  const commitId = process.env.GITHUB_SHA;
  const repository = process.env.GITHUB_REPOSITORY;
  const [owner, repo] = repository.split("/");
  const pullRequestNumber = process.env.GITHUB_PR_NUMBER;

  const reviewsFilePath = path.resolve("reviews.txt");
  const reviews = fs.readFileSync(reviewsFilePath, "utf-8").split("\n");

  let fileName = "";
  let diff = "";
  let review = "";
  let comments = [];

  reviews.forEach((line) => {
    if (line.startsWith("FILE: ")) {
      fileName = line.replace("FILE: ", "");
    } else if (line.startsWith("DIFF: ")) {
      diff = "";
    } else if (line.startsWith("REVIEW: ")) {
      review = "";
    } else if (line.startsWith("ENDREVIEW")) {
      comments.push({ fileName, diff, review });
    } else if (line.startsWith("ENDDIFF")) {
      // Do nothing
    } else if (diff !== undefined) {
      diff += `${line}\n`;
    } else {
      review += `${line}\n`;
    }
  });

  for (const comment of comments) {
    const { fileName, review } = comment;
    const hunkHeader = /@@ -(\d+),(\d+) \+(\d+),(\d+) @@/.exec(comment.diff);
    if (!hunkHeader) continue;

    const [_, originalStartLine, , newStartLine] = hunkHeader;
    const side = comment.diff.startsWith("-") ? "LEFT" : "RIGHT";
    const startLine = side === "LEFT" ? parseInt(originalStartLine, 10) : parseInt(newStartLine, 10);

    await octokit.pulls.createReviewComment({
      owner,
      repo,
      pull_number: pullRequestNumber,
      commit_id: commitId,
      body: review,
      path: fileName,
      line: startLine,
      side: side,
    });
  }
}

postComments().catch((error) => {
  console.error("Error posting comments:", error);
  process.exit(1);
});
