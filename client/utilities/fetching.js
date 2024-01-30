export default async function fetching(resource, method = "GET", body = null) {
  const res = await fetch(resource, {
    method: method,
    body: body,
  });
  const json = await res.json();
  console.log(resource, json);
  return json;
}
