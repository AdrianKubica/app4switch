import axios from 'axios'

export class SwitchAPI {
    static async getSwitchData(formData: any) {
        try {
            const res = await axios.post('/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            return res.data
        } catch(err) {
            console.log(err.msg)
        }
    }

}