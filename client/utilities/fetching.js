export default async function fetching(
  resource,
  credentials = "same-origin",
  method = "GET",
) {
  const res = await fetch(resource, {
    method: method,
    credentials: credentials,
  });
  const json = await res.json();
  console.log(resource, json);
  return json;
}
