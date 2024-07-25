async function postCommentToGitHub(escaped_comments, commit_id, file_path, start_line, side) {
  const { Octokit } = await import('@octokit/core');
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
  
  console.log(escaped_comments);
  console.log(commit_id);
  console.log(file_path);
  console.log(start_line);
  console.log(side);
  
  const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');

  console.log(owner);
  console.log(repo);
  
  const response = await octokit.issues.createComment({
        repo,
        owner,
        issue_number: process.env.GITHUB_EVENT_NUMBER,
        body: escaped_comments
        });

  if (response.status !== 201) {
    throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
  }

  return response.data;
}

const args = process.argv.slice(2);

if (args.length < 5) {
  console.error('Insufficient arguments. Expected: escaped_comments, commit_id, file_path, start_line, side');
  process.exit(1);
}

const [escaped_comments, commit_id, file_path, start_line, side] = args;

postCommentToGitHub(escaped_comments, commit_id, file_path, start_line, side)
  .then(response => console.log('Comment posted successfully:', response))
  .catch(error => console.error('Error posting comment:', error));
