import { faFile } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';

//  import '../../scss/components/Common/FilesDragAndDrop.scss';

export default function FilesDragAndDrop({onUpload}) {
  return (
    <div className='w-full h-96 flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-md gap-3'>
        <FontAwesomeIcon icon={faFile} className='fa-2xl text-gray-200'/>
        <div className='text-gray-200 text-xl'>Drop your documents here or</div>
        <input type='file' onChange={onUpload} className='border text-gray-200 text-xs file:bg-blue-200' />
    </div>
  );
}

FilesDragAndDrop.propTypes = {
  onUpload: PropTypes.func.isRequired,
};