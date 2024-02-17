export default async function fetching(
  resource,
  method = "GET",
  body = null,
  headers = {},
) {
  const res = await fetch(resource, {
    method: method,
    body: body,
    headers: headers,
  });
  const json = await res.json();
  console.log(resource, json);
  return json;
}
