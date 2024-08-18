import {Layout} from 'layouts/Layout'

export default  function Home() {
  return (
    <Layout className='backdrop-brightness-150' fixed>
      <Layout.Header sticky>
        <span>header</span>
      </Layout.Header>

      <Layout.Body>
          <span>body</span>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae eveniet blanditiis quidem placeat ex laborum hic, magnam aut temporibus numquam nihil veritatis eaque saepe iure, eum reiciendis odit dolorem harum!
          Facere, consectetur numquam voluptas eligendi vero quasi saepe, ad consequatur quis blanditiis alias eius iste unde, doloribus repellat. Laborum aliquid asperiores totam, dolores hic quae libero maxime explicabo distinctio autem.
          Sunt voluptates, exercitationem, iste temporibus dicta unde, perferendis ipsam voluptatum harum magni voluptate? Quis consequatur ullam quibusdam animi at sed iste suscipit, excepturi quos fugit incidunt, doloremque ipsam repellat. Amet!
          Explicabo asperiores nihil reiciendis necessitatibus velit aut omnis ad laboriosam iure officia. Saepe omnis animi vero dolor nam necessitatibus, nostrum, culpa adipisci aut iure, perferendis amet ut quos quaerat aperiam.
          Eius possimus maxime sunt molestias quibusdam labore? Officia facere earum error dicta blanditiis deleniti. Dolore blanditiis saepe nobis quia distinctio, unde officiis, sed laboriosam doloribus a odit eaque suscipit ut!
      
          
          </Layout.Body>

      <Layout.Footer>
          <span>footer</span>
      </Layout.Footer>
    </Layout>
  );
}