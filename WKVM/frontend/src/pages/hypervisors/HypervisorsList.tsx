import { Layout } from 'layouts/Layout'
import { data } from 'data/example'
import { columns, Payment } from 'data/columns'
import { DataTable } from 'components/DataTable'

export default function HypervisorsList() {
    return (
        <Layout fixed>
            <Layout.Header sticky>
                ww
            </Layout.Header>

            <Layout.Body>
                <span>body</span>
                <DataTable columns={columns} data={data} />
                
                </Layout.Body>

            <Layout.Footer>
                
            </Layout.Footer>
        </Layout>
    );
}
